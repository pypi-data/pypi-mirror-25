import os


class Line():

    def __init__(self, line:str):
        self.line = line

        if line.find('[') != -1:
            line, tag = line.split('[')
            self.line = line.rstrip() # remove space
            self.tag = tag.strip(']')
        else:
            self.tag = None

    @property
    def tag_exists(self):
        return self.tag != None

    def has_tag(self, tag):
        return self.tag == tag

    def remove_tag(self):
        self.tag = None

    def __eq__(self, other):
        return self.line == other.line

    def __str__(self):
        s = self.line
        if self.tag is not None:
            s = s + f' [{self.tag}]'
        return s

    def __repr__(self):
        return str(self)


class TallyLog():

    _DOWN = 1
    _UP = -1

    def __init__(self, filename):
        self.filename = filename
        self._lines = self._read_lines()

    @property
    def lines(self):
        return list(map(lambda line: str(line), self._lines))

    @property
    def tagless_lines(self):
        return [str(line) for line in self._lines if not line.tag_exists]

    def add(self, line):
        self._lines.append(Line(line))
        self._commit()

    def line(self, tag):
        """Return line with tag. Tag is not included in line"""
        found = [line for line in self._lines if line.has_tag(tag)]
        if not found:
            raise TagNotFound()
        return found[0].line

    def line_tag(self, line):
        line = self._find_line(Line(line))
        if line is None:
            raise NoSuchLineFound()
        return line.tag

    def remove_first(self):
        """Removes first line"""
        self._lines = self._lines[1:]
        self._commit()

    def remove_line(self, line):
        """Removes line which matches line, line can contain tag"""
        try:
            self._lines.remove(Line(line))
        except ValueError:
            raise NoSuchLineFound()
        self._commit()

    def tag(self, line_to_be_tagged:str, tag:str):
        line_to_tag = self._find_line(Line(line_to_be_tagged))
        if line_to_tag is None:
            raise NoSuchLineFound()
        line_to_tag.tag = tag
        self._commit()

    def remove_tag(self, tag):
        """Removes all tags"""
        self._remove_tags(tag)
        self._commit()

    def move_tag(self, from_line:str, to_line:str):
        """Removes tags from other lines and adds it to
        the 'line_to_be_tagged'. If tag does not exists it is just
        added.
        """
        fl = self._find_line_or_raise(Line(from_line))
        if not fl.tag_exists:
            raise TagNotFound()
        tl = self._find_line_or_raise(Line(to_line))
        tl.tag = fl.tag
        fl.remove_tag()
        self._commit()

    def move_tag_up(self, tag):
        self._move_tag(tag, self._UP)

    def move_tag_down(self, tag):
        self._move_tag(tag, self._DOWN)

    def change_tag(self, tag_to_change, new_tag):
        positions = self._tag_positions(tag_to_change)
        lines = [self._lines[position] for position in positions]
        for line in lines:
            self.tag(line.line, new_tag)

    def _find_line_or_raise(self, line:Line) -> Line:
        l = self._find_line(line)
        if l is None:
            raise NoSuchLineFound()
        return l

    def _find_line(self, line:Line) -> Line:
        for l in self._lines:
            if line == l:
                return l
        return None

    def _move_tag(self, tag, direction):
        tag_positions = self._tag_positions(tag)

        new_tag_positions = [tag_pos + direction for tag_pos in tag_positions]

        if any([tag_pos < 0 or tag_pos > len(self._lines)-1 for tag_pos in  new_tag_positions]):
            raise CannotMoveTag()

        lines_to_be_tagged = [self._lines[tag_pos] for tag_pos in new_tag_positions]

        self._remove_tags(tag)

        for line_to_be_tagged in lines_to_be_tagged:
            line_to_be_tagged.tag = tag
        self._commit()


    def _remove_tags(self, tag):
        for line in self._lines:
            if line.has_tag(tag):
                line.remove_tag()

    def _tag_positions(self, tag):
        tag_lines = filter(lambda line: line.has_tag(tag), self._lines)
        positions = [self._lines.index(tag_line) for tag_line in tag_lines]
        if positions == []:
            raise TagNotFound()
        return positions

    def _read_lines(self):
        if not os.path.exists(self.filename):
            return []

        with open(self.filename, 'rt') as f:
            return [Line(line.rstrip()) for line in f]

    def _commit(self):
        with open(self.filename, 'wt') as f:
            f.writelines([str(line) + os.linesep for line in self._lines])

class NoSuchLineFound(Exception):
    pass

class TagNotFound(Exception):
    pass

class CannotMoveTag(Exception):
    pass
