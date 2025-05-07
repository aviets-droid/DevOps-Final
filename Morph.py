class Morph(object):
    name = ""
    isVisible = False
    level = ""
    associatedHealthIssue = ""
    issueDesc = ""

    def __init__(
        self,
        name,
        isVisible,
        level,
        associatedHealthIssue,
        issueDesc
    ):
        self.name = name
        self.isVisible = isVisible
        self.level = level
        self.associatedHealthIssue = (
            associatedHealthIssue
        )
        self.issueDesc = issueDesc

    def setMorphName(self, name):
        self.name = name

    def getMorphName(self):
        return self.name

    def getMorphIssue(self):
        return self.associatedHealthIssue

    def getMorphVisibility(self):
        return self.isVisible

    def setMorphVisibility(self, visibility: bool):
        if isinstance(visibility, bool):
            self.isVisible = visibility
        else:
            raise TypeError(
                "Visibility is supposed to be a boolean value."
                )
