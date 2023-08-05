import os


class Tally:

    _DOWN = 1
    _UP = -1

    def __init__(self, filename):
        self.filename = filename

    @property
    def lines(self):
        with open(self.filename, 'rt') as f:
            return [line.rstrip() for line in f.readlines()]

    def add(self, line):
        with open(self.filename, 'at') as f:
            f.write(line + os.linesep)

    def line(self, tag):
        """Return line with tag. Tag is not included in line"""
        lines = self.lines
        tag_positions = self._tag_positions(tag, lines)
        if not tag_positions:
            raise TagNotFound()
        return self._strip_tag(lines[tag_positions[0]])

    def tag(self, line_to_be_tagged, tag):
        updated_lines = self._add_tag_to_lines(line_to_be_tagged, tag, self.lines)

        self._raise_exception_if_tag_not_set(updated_lines, tag)

        self._overwrite_tally(updated_lines)

    def remove_tag(self, tag):
        with open(self.filename, 'rt') as f:
            updated_lines = self._remove_tag(tag, f)
        self._overwrite_tally(updated_lines)

    def move_tag(self, line_to_be_tagged, tag):
        """Removes tags from other lines and adds it to
        the 'line_to_be_tagged'. If tag does not exists it is just
        added.
        """
        self.remove_tag(tag)
        self.tag(line_to_be_tagged, tag)

    def move_tag_up(self, tag):
        self._move_tag(tag, self._UP)

    def move_tag_down(self, tag):
        self._move_tag(tag, self._DOWN)

    def remove_first(self):
        updated_lines = self.lines[1:]
        self._overwrite_tally(updated_lines)

    def _move_tag(self, tag, direction):
        lines = self.lines
        tag_positions = self._tag_positions(tag, lines)

        new_tag_positions = [tag_pos + direction for tag_pos in tag_positions]

        if tag_positions == []:
            raise TagNotFound()
        if any([tag_pos < 0 or tag_pos > len(lines)-1 for tag_pos in  new_tag_positions]):
            raise CannotMoveTag()

        lines_to_be_tagged = [lines[tag_pos] for tag_pos in new_tag_positions]

        lines = self._remove_tag(tag, lines)
        for line_to_be_tagged in lines_to_be_tagged:
            lines = self._add_tag_to_lines(line_to_be_tagged, tag, lines)
        self._overwrite_tally(lines)

    def _add_tag_to_lines(self, line_to_be_tagged, tag, iterable):
        return [self._add_tag_if_match(line_to_be_tagged, line, tag) for line in iterable]

    def _remove_tag(self, tag, iterable):
        return [self._strip_tag(line) for line in iterable]

    def _add_tag_if_match(self, line_to_be_tagged, line, tag):
        tagless_line = self._strip_tag(line)
        if line_to_be_tagged == tagless_line:
            return tagless_line + f' [{tag}]'
        return line

    def _overwrite_tally(self, lines):
        with open(self.filename, 'wt') as f:
            f.writelines([line + os.linesep for line in lines])

    def _raise_exception_if_tag_not_set(self, lines, tag):
        if not any([tag in line for line in lines]):
            raise NoSuchLineFound()

    def _strip_tag(self, line):
        return line.split('[')[0].rstrip()

    def _tag_positions(self, tag, lines):
        tag_lines = filter(lambda line: tag in line, lines)
        return [lines.index(tag_line) for tag_line in tag_lines]

class NoSuchLineFound(Exception):
    pass

class TagNotFound(Exception):
    pass

class CannotMoveTag(Exception):
    pass
