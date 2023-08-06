from PyQt5 import QtCore
class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None

def iterator2dataframes(iterator, chunk_size: int):
    records = []
    frames = []
    for i, record in enumerate(iterator):
        records.append(record)
        if i % chunk_size == chunk_size - 1:
            frames.append(pd.DataFrame(records))
            records = []
    if records:
        frames.append(pd.DataFrame(records))
    return pd.concat(frames)

keywords = [
        "use", "select", "as", "then", "case", "end",
        "from", "where", "group by", "order by", "desc", "asc",
        "distinct", "on", "left join", "right join", "count",
        "sum", "max", "min","distinct", "and", "in", "or",
        "date","NOW", "like",
    ]

    # Python operators
operators = [
        "&&", "between", "binary", "&",
        "\\^", "=", ">=", ">",
        "is null", "null", "<=", "<",
        " like ", "regexp", "not", ";",",",
    ]

    # Python braces
braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]


"""
void MyWidget::paintEvent(QPaintEvent* /*event*/) {
 QColor backgroundColor = palette().light().color();
 backgroundColor.setAlpha(200);
 QPainter customPainter(this);
 customPainter.fillRect(rect(),backgroundColor);
}
"""

"""
def keyPressEvent(self, event):
    key = event.key()
    if key == Qt.Key_Enter:
        #For Enter of keyboard number
        print("key Enter press")
        self.updateUi()
    if key == Qt.Key_Return:
        #For Enter of keyboard
        print("key Enter press")
        self.updateUi()
"""
