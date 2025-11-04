import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

ApplicationWindow {
  id: win
  width: 1100
  height: 720
  visible: true
  title: "Editor - Normalização (RGB/RGBA) + Cinza + Seleção"

  property bool dragging: false
  property real imgLeft: 0
  property real imgTop: 0
  property real imgW: 0
  property real imgH: 0
  property int  x0: 0
  property int  y0: 0
  property int  x1: 0
  property int  y1: 0

  header: ToolBar {
    RowLayout {
      anchors.fill: parent
      spacing: 12

      ToolButton {
        text: "Abrir imagem"
        onClicked: fileDialog.open()
      }

      ButtonGroup { id: modeGroup }
      RadioButton {
        text: "Cor (RGB/RGBA)"
        checked: true
        ButtonGroup.group: modeGroup
        onToggled: if (checked) imageVM.setActive("color")
      }
      RadioButton {
        text: "Cinza"
        ButtonGroup.group: modeGroup
        onToggled: if (checked) imageVM.setActive("gray")
      }

      Item { Layout.fillWidth: true }

      Label {
        text: `Seleção: (${x0},${y0}) → (${x1},${y1})  |  Dim: ${Math.abs(x1-x0)}x${Math.abs(y1-y0)}`
        font.bold: true
      }

      ComboBox {
        id: filterCombo
        model: imageVM.filters
        textRole: "name"
        valueRole: "key"
        Layout.preferredWidth: 220
      }

      ToolButton {
        text: "Aplicar filtro"
        onClicked: {
          // Exemplo: Blur usa argumento; Gray não precisa
          const key = filterCombo.currentValue
          const args = key === "blur" ? { radius: 4.0 } : {}
          imageVM.applyFilter(key, args)
        }
      }
    }
  }

  FileDialog {
    id: fileDialog
    title: "Selecione uma imagem"
    nameFilters: ["Imagens (*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.webp)"]
    onAccepted: imageVM.openImage(selectedFile)
  }

  Rectangle {
    id: stage
    anchors.fill: parent
    color: "#1e1e1e"

    Item {
      id: imgContainer
      anchors.fill: parent
      anchors.margins: 16

      Image {
        id: img
        source: imageVM.activeMode === "gray" ? imageVM.grayUrl : imageVM.colorUrl
        asynchronous: true
        fillMode: Image.PreserveAspectFit
        smooth: true
        cache: false
        anchors.fill: parent

        onPaintedWidthChanged: updatePaintedRect()
        onPaintedHeightChanged: updatePaintedRect()
        onStatusChanged: { if (status === Image.Ready) updatePaintedRect() }

        function updatePaintedRect() {
          imgW = paintedWidth
          imgH = paintedHeight
          imgLeft = (width - paintedWidth) / 2
          imgTop  = (height - paintedHeight) / 2
        }

        Rectangle {
          id: selectionRect
          visible: dragging || (x0 !== x1 && y0 !== y1)
          color: "#33FFFFFF"
          border.color: "#00A8FF"
          border.width: 2
          radius: 2
          x: Math.min(mouseLayer.selX, mouseLayer.curX)
          y: Math.min(mouseLayer.selY, mouseLayer.curY)
          width: Math.abs(mouseLayer.curX - mouseLayer.selX)
          height: Math.abs(mouseLayer.curY - mouseLayer.selY)

          Repeater {
            model: 3
            Rectangle {
              width: parent.width
              height: 1
              y: (index + 1) * parent.height / 4
              color: "#55FFFFFF"
            }
          }
          Repeater {
            model: 3
            Rectangle {
              height: parent.height
              width: 1
              x: (index + 1) * parent.width / 4
              color: "#55FFFFFF"
            }
          }
        }

        MouseArea {
          id: mouseLayer
          anchors.fill: parent
          hoverEnabled: true
          property real selX: 0
          property real selY: 0
          property real curX: 0
          property real curY: 0

          function clampToImage(px, py) {
            var cx = Math.max(imgLeft, Math.min(imgLeft + imgW, px))
            var cy = Math.max(imgTop,  Math.min(imgTop  + imgH, py))
            return { px: cx, py: cy }
          }

          function toImageCoords(px, py) {
            var c = clampToImage(px, py)
            var nx = (c.px - imgLeft) / imgW
            var ny = (c.py - imgTop)  / imgH

            var iw = imageVM.imageWidth
            var ih = imageVM.imageHeight
            if (iw <= 0 || ih <= 0) {
              iw = imgW; ih = imgH
            }

            var ix = Math.round(nx * iw)
            var iy = Math.round(ny * ih)
            return { ix: ix, iy: iy, px: c.px, py: c.py }
          }

          onPressed: (mouse) => {
            if (img.status !== Image.Ready) return
            dragging = true
            var c = toImageCoords(mouse.x, mouse.y)
            selX = c.px; selY = c.py
            curX = c.px; curY = c.py
            x0 = c.ix; y0 = c.iy
            x1 = c.ix; y1 = c.iy
          }
          onPositionChanged: (mouse) => {
            if (!dragging) return
            var c = toImageCoords(mouse.x, mouse.y)
            curX = c.px; curY = c.py
            x1 = c.ix; y1 = c.iy
          }
          onReleased: (mouse) => {
            if (!dragging) return
            var c = toImageCoords(mouse.x, mouse.y)
            curX = c.px; curY = c.py
            x1 = c.ix; y1 = c.iy
            dragging = false
            imageVM.updateSelection(x0, y0, x1, y1)
          }
        }
      }
    }
  }

  footer: ToolBar {
    RowLayout { anchors.fill: parent; spacing: 12
      Label { text: "Modo ativo: " + imageVM.activeMode.toUpperCase() }
      Item { Layout.fillWidth: true }
      Label { text: "Dica: arraste sobre a imagem para selecionar um retângulo." }
    }
  }
}
