"""
Data structures for the schemas
of C4.5 data sets
"""
import re
import sys
import collections

###############################################################################
#                     CODE FOR FEATURES, EXAMPLES, ETC.                       #
###############################################################################

class Feature(object):
    """
    Information for a feature
    of C4.5 data
    """

    class Type:
        """
        Type of feature
        """
        CLASS      = 'CLASS'
        ID         = 'ID'
        BINARY     = 'BINARY'
        NOMINAL    = 'NOMINAL'
        CONTINUOUS = 'CONTINUOUS'

    def __init__(self, name, ftype, values=None):
        self.name = name
        self.type = ftype
        if (self.type == Feature.Type.ID or
            self.type == Feature.Type.NOMINAL):
            if values is None:
                raise Exception('No values for %s feature' % self.type)
            else:
                self.values = tuple(values)
        else:
            if values is None:
                self.values = None
            else:
                raise Exception('Values given for % feature' % self.type)
        self.tup = (self.name, self.type, self.values)

    def __cmp__(self, other):
        if self.tup > other.tup:
            return 1
        elif self.tup < other.tup:
            return -1
        else:
            return 0

    def __hash__(self):
        return self.tup.__hash__()

    def __repr__(self):
        return '<%s, %s, %s>' % self.tup

    def to_float(self, value):
        if value is None:
            return None
        if (self.type == Feature.Type.ID or
            self.type == Feature.Type.NOMINAL):
            return float(self.values.index(value))
        elif (self.type == Feature.Type.BINARY or
              self.type == Feature.Type.CLASS):
            if value: return 1.0
            else:     return 0.0
        else:
            return value


Feature.CLASS = Feature("CLASS", Feature.Type.CLASS)

class Schema(collections.Sequence):
    """
    Represents a schema for C4.5 data
    """

    def __init__(self, features):
        self.features = tuple(features)

    def __cmp__(self, other):
        if self.features > other.features:
            return 1
        elif self.features < other.features:
            return -1
        else:
            return 0

    def __hash__(self):
        return self.features.__hash__()

    def __repr__(self):
        return str(self.features)

    def __len__(self):
        return len(self.features)

    def __iter__(self):
        return self.features.__iter__()

    def __contains__(self, item):
        return self.features.__contains__(item)

    def __getitem__(self, key):
        return self.features[key]
"""
Data structures for storing examples
and sets of examples
"""

class ExampleSet(collections.MutableSequence):
    """
    Holds a set of examples
    """
    def __init__(self, schema):
        self.schema = schema
        self.examples = []

    def __len__(self):
        return len(self.examples)

    def __iter__(self):
        return self.examples.__iter__()

    def __contains__(self, item):
        return self.examples.__contains__(item)

    def __getitem__(self, key):
        return self.examples[key]

    def __setitem__(self, key, example):
        if example.schema != self.schema:
            raise ValueError('Schema mismatch')
        self.examples[key] = example

    def __delitem__(self, key):
        del self.examples[key]

    def insert(self, key, example):
        if example.schema != self.schema:
            raise ValueError('Schema mismatch')
        return self.examples.insert(key, example)

    def append(self, example):
        if example.schema != self.schema:
            raise ValueError('Schema mismatch')
        super(ExampleSet,self).append(example)

    def __repr__(self):
        return '<%s, %s>' % (self.schema, self.examples)

    def to_float(self, normalizer=None):
        return [ex.to_float(normalizer) for ex in self]

class Example(collections.MutableSequence):
    """
    Represents a single example
    from a dataset
    """
    def __init__(self, schema):
        self.schema = schema
        self.features = [None for i in range(len(schema))]
        self.weight = 1.0

    def __len__(self):
        return len(self.features)

    def __iter__(self):
        return self.features.__iter__()

    def __contains__(self, item):
        return self.features.__contains__(item)

    def __getitem__(self, key):
        return self.features[key]

    def __setitem__(self, key, value):
        self.features[key] = value

    def __delitem__(self, key):
        del self.features[key]

    def insert(self, key, item):
        return self.features.insert(key, item)

    def __repr__(self):
        return '<%s, %s, %s>' % (self.schema, self.features, self.weight)

    def to_float(self, normalizer=None):
        if normalizer is None:
            normalizer = lambda x: x
        return normalizer([feature.to_float(value)
                           for feature, value in zip(self.schema, self)])

###############################################################################
#                            CODE TO PARSE C4.5                               #
###############################################################################

_NAMES_EXT = '.names'
_DATA_EXT = '.data'

_COMMENT_RE = '//.*'
_BINARY_RE = '\\s*0\\s*,\\s*1\\s*'

def parse_c45(file_base, rootdir='.'):
    """
    Returns an ExampleSet from the parsed C4.5-formatted data file

    Arguments:
    file_base -- basename of the file, as in 'file_base.names'
    rootdir   -- root of directory tree to search for files

    """
    schema_name = file_base + _NAMES_EXT
    schema_filename = _find_file(schema_name, rootdir)
    if schema_filename is None:
        raise ValueError('Schema file not found')

    data_name = file_base + _DATA_EXT
    data_filename = _find_file(data_name, rootdir)
    if data_filename is None:
        raise ValueError('Data file not found')

    return _parse_c45(schema_filename, data_filename)

def _parse_c45(schema_filename, data_filename):
    """Parses C4.5 given file names"""
    try:
        schema = _parse_schema(schema_filename)
    except Exception as e:
        raise Exception('Error parsing schema: %s' % e)

    try:
        examples = _parse_examples(schema, data_filename)
    except Exception as e:
        raise Exception('Error parsing examples: %s' % e)

    return examples

def _parse_schema(schema_filename):
    """Parses C4.5 '.names' schema file"""
    features = []
    needs_id = True
    with open(schema_filename) as schema_file:
        for line in schema_file:
            feature = _parse_feature(line, needs_id)
            if feature is not None:
                if (needs_id and feature.type == Feature.Type.ID):
                    needs_id = False
                features.append(feature)

    # Fix the problem that the class feature is listed first in the
    # '.names' file, but is the last feature in the '.data' file
    try:
        features.remove(Feature.CLASS)
    except:
        raise Exception('File does not contain "Class" line')
    features.append(Feature.CLASS)

    return Schema(features)

def _parse_feature(line, needs_id):
    """
    Parse a feature from the given line. The second argument
    indicates whether we need an ID for our schema, in which
    case the first non-CLASS feature is selected.

    """
    line = _trim_line(line)
    if len(line) == 0:
        # Blank line
        return None
    if re.match(_BINARY_RE, line) is not None:
        # Class feature
        return Feature.CLASS
    colon = line.find(':')
    if colon < 0:
        raise Exception('No feature name found.')
    name = line[:colon].strip()
    remainder = line[colon + 1:]
    values = _parse_values(remainder)
    if needs_id:
        return feature(name, feature.type.id, values)
    elif len(values) == 1 and values[0].startswith('continuous'):
        return feature(name, feature.type.continuous)
    elif len(values) == 2 and '0' in values and '1' in values:
        return feature(name, feature.type.binary)
    else:
        return feature(name, feature.type.nominal, values)

def _parse_values(value_string):
    """Parse comma-delimited values from a string"""
    values = list()
    for raw in value_string.split(','):
        raw = raw.strip()
        if len(raw) > 1 and raw[0] == '"' and raw[-1] == '"':
            raw = raw[1:-1].strip()
        values.append(raw)
    return values

def _parse_examples(schema, data_filename):
    """Parse examples from a '.data' file given a schema"""
    exset = ExampleSet(schema)
    with open(data_filename) as data_file:
        for line in data_file:
            line = _trim_line(line)
            if len(line) == 0:
                # Skip blank line
                continue
            try:
                ex = _parse_example(schema, line)
                exset.append(ex)
            except Exception as e:
                import traceback
                traceback.print_exc(file=sys.stderr)
                print >> sys.stderr, 'Warning: skipping line: "%s"' % line

    return exset

def _parse_example(schema, line):
    """Parse a single example from the line of a data file"""
    values = _parse_values(line)
    if len(values) != len(schema):
        raise Exception('Feature-data size mismatch: %s' % line)

    ex = Example(schema)
    for i, value in enumerate(values):
        if value == '?':
            # Unknown value remains 'None'
            continue

        # Cast to proper type
        stype = schema[i].type
        if (stype == Feature.Type.ID or
            stype == Feature.Type.NOMINAL):
            ex[i] = value
        elif (stype == Feature.Type.BINARY or
              stype == Feature.Type.CLASS):
            ex[i] = bool(int(value))
        elif stype == Feature.Type.CONTINUOUS:
            ex[i] = float(value)
        else:
            raise ValueError('Unknown schema type "%s"' % stype)

    return ex

def _trim_line(line):
    """Removes comments and periods from the given line"""
    line = re.sub(_COMMENT_RE, '', line)
    line = line.strip()
    if len(line) > 0 and line[-1] == '.':
        line = line[:-1].strip()
    return line

def _find_file(filename, rootdir):
    """
    Finds a file with filename located in some
    subdirectory of the root directory
    """
    import os
    for dirpath, _, filenames in os.walk(rootdir):
        if filename in filenames:
            return os.path.join(dirpath, filename)
