class Weeder:    
    def weed(self, items):
        for item in items:
            if not self._satisfactory(item):
                self.items.pop(item)
    
    def _satisfactory(self, item):
        if (
                (
                    item['format'] == 'x264' or
                    item['format'] == 'h264'
                 ) and
                (
                    item['resolution'] == '1080' or
                    item['resolution'] == '720'
                )
        ):
            return True
        else:
            return False

    def sort(self, items, criteria):
        sorted = []
        for item in items:
            for criterion_type, criterion in criteria.items():
                if self._satisfies(item, criterion, criterion_type):
                    sorted.append(item)
        return sorted
    
    def _satisfies(self, item, criterion, criterion_type):
        if item[criterion_type] == criterion:
            return True
        else:
            return False
