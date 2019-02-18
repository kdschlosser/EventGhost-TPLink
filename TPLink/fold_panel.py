# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import wx
import tp_link
import datetime
import cStringIO
import wx.lib.scrolledpanel as scrolled
import wx.lib.agw.foldpanelbar as fpb
from wx import calendar
from wx.lib.masked import timectrl


def collapsed_icon_data():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x8eIDAT8\x8d\xa5\x93-n\xe4@\x10\x85?g\x03\n6lh)\xc4\xd2\x12\xc3\x81\
\xd6\xa2I\x90\x154\xb9\x81\x8f1G\xc8\x11\x16\x86\xcd\xa0\x99F\xb3A\x91\xa1\
\xc9J&\x96L"5lX\xcc\x0bl\xf7v\xb2\x7fZ\xa5\x98\xebU\xbdz\xf5\\\x9deW\x9f\xf8\
H\\\xbfO|{y\x9dT\x15P\x04\x01\x01UPUD\x84\xdb/7YZ\x9f\xa5\n\xce\x97aRU\x8a\
\xdc`\xacA\x00\x04P\xf0!0\xf6\x81\xa0\xf0p\xff9\xfb\x85\xe0|\x19&T)K\x8b\x18\
\xf9\xa3\xe4\xbe\xf3\x8c^#\xc9\xd5\n\xa8*\xc5?\x9a\x01\x8a\xd2b\r\x1cN\xc3\
\x14\t\xce\x97a\xb2F0Ks\xd58\xaa\xc6\xc5\xa6\xf7\xdfya\xe7\xbdR\x13M2\xf9\
\xf9qKQ\x1fi\xf6-\x00~T\xfac\x1dq#\x82,\xe5q\x05\x91D\xba@\xefj\xba1\xf0\xdc\
zzW\xcff&\xb8,\x89\xa8@Q\xd6\xaaf\xdfRm,\xee\xb1BDxr#\xae\xf5|\xddo\xd6\xe2H\
\x18\x15\x84\xa0q@]\xe54\x8d\xa3\xedf\x05M\xe3\xd8Uy\xc4\x15\x8d\xf5\xd7\x8b\
~\x82\x0fh\x0e"\xb0\xad,\xee\xb8c\xbb\x18\xe7\x8e;6\xa5\x89\x04\xde\xff\x1c\
\x16\xef\xe0p\xfa>\x19\x11\xca\x8d\x8d\xe0\x93\x1b\x01\xd8m\xf3(;x\xa5\xef=\
\xb7w\xf3\x1d$\x7f\xc1\xe0\xbd\xa7\xeb\xa0(,"Kc\x12\xc1+\xfd\xe8\tI\xee\xed)\
\xbf\xbcN\xc1{D\x04k\x05#\x12\xfd\xf2a\xde[\x81\x87\xbb\xdf\x9cr\x1a\x87\xd3\
0)\xba>\x83\xd5\xb97o\xe0\xaf\x04\xff\x13?\x00\xd2\xfb\xa9`z\xac\x80w\x00\
\x00\x00\x00IEND\xaeB`\x82'


def expanded_icon_data():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x9fIDAT8\x8d\x95\x93\xa1\x8e\xdc0\x14EO\xb2\xc4\xd0\xd2\x12\xb7(mI\
\xa4%V\xd1lQT4[4-\x9a\xfe\xc1\xc2|\xc6\xc2~BY\x83:A3E\xd3\xa0*\xa4\xd2\x90H!\
\x95\x0c\r\r\x1fK\x81g\xb2\x99\x84\xb4\x0fY\xd6\xbb\xc7\xf7>=\'Iz\xc3\xbcv\
\xfbn\xb8\x9c\x15 \xe7\xf3\xc7\x0fw\xc9\xbc7\x99\x03\x0e\xfbn0\x99F+\x85R\
\x80RH\x10\x82\x08\xde\x05\x1ef\x90+\xc0\xe1\xd8\ryn\xd0Z-\\A\xb4\xd2\xf7\
\x9e\xfbwoF\xc8\x088\x1c\xbbae\xb3\xe8y&\x9a\xdf\xf5\xbd\xe7\xfem\x84\xa4\
\x97\xccYf\x16\x8d\xdb\xb2a]\xfeX\x18\xc9s\xc3\xe1\x18\xe7\x94\x12cb\xcc\xb5\
\xfa\xb1l8\xf5\x01\xe7\x84\xc7\xb2Y@\xb2\xcc0\x02\xb4\x9a\x88%\xbe\xdc\xb4\
\x9e\xb6Zs\xaa74\xadg[6\x88<\xb7]\xc6\x14\x1dL\x86\xe6\x83\xa0\x81\xba\xda\
\x10\x02x/\xd4\xd5\x06\r\x840!\x9c\x1fM\x92\xf4\x86\x9f\xbf\xfe\x0c\xd6\x9ae\
\xd6u\x8d \xf4\xf5\x165\x9b\x8f\x04\xe1\xc5\xcb\xdb$\x05\x90\xa97@\x04lQas\
\xcd*7\x14\xdb\x9aY\xcb\xb8\\\xe9E\x10|\xbc\xf2^\xb0E\x85\xc95_\x9f\n\xaa/\
\x05\x10\x81\xce\xc9\xa8\xf6><G\xd8\xed\xbbA)X\xd9\x0c\x01\x9a\xc6Q\x14\xd9h\
[\x04\xda\xd6c\xadFkE\xf0\xc2\xab\xd7\xb7\xc9\x08\x00\xf8\xf6\xbd\x1b\x8cQ\
\xd8|\xb9\x0f\xd3\x9a\x8a\xc7\x08\x00\x9f?\xdd%\xde\x07\xda\x93\xc3{\x19C\
\x8a\x9c\x03\x0b8\x17\xe8\x9d\xbf\x02.>\x13\xc0n\xff{PJ\xc5\xfdP\x11""<\xbc\
\xff\x87\xdf\xf8\xbf\xf5\x17FF\xaf\x8f\x8b\xd3\xe6K\x00\x00\x00\x00IEND\xaeB\
`\x82'


def convert_icon(icon_data):
    stream = cStringIO.StringIO(icon_data)
    image = wx.ImageFromStream(stream)
    stream.close()
    return wx.BitmapFromImage(image)

try:
    COLLAPSED_ICON = convert_icon(collapsed_icon_data())
    EXPANDED_ICON = convert_icon(expanded_icon_data())

    IMAGE_LIST = wx.ImageList(16, 16)
    IMAGE_LIST.Add(COLLAPSED_ICON)
    IMAGE_LIST.Add(EXPANDED_ICON)
except:
    pass


_fold_panel_item = fpb.FoldPanelItem


class CaptionBar(wx.Window):
    def __init__(
        self,
        parent,
        id,
        pos,
        size,
        caption="",
        foldIcons=None,
        cbstyle=None,
        rightIndent=fpb.FPB_BMP_RIGHTSPACE,
        iconWidth=16,
        iconHeight=16,
        collapsed=False
    ):

        wx.Window.__init__(
            self,
            parent,
            wx.ID_ANY,
            pos=pos,
            size=(20, 20),
            style=wx.NO_BORDER
        )

        self._controlCreated = False
        self._collapsed = collapsed
        self.ApplyCaptionStyle(cbstyle, True)

        if foldIcons is None:
            foldIcons = wx.ImageList(16, 16)

            bmp = fpb.ExpandedIcon.GetBitmap()
            foldIcons.Add(bmp)
            bmp = fpb.CollapsedIcon.GetBitmap()
            foldIcons.Add(bmp)

        # set initial size
        if foldIcons:
            assert foldIcons.GetImageCount() > 1
            iconWidth, iconHeight = foldIcons.GetSize(0)

        self._caption = caption
        self._foldIcons = foldIcons
        self._style = cbstyle
        self._rightIndent = rightIndent
        self._iconWidth = iconWidth
        self._iconHeight = iconHeight
        self._oldSize = wx.Size(20, 20)

        self._controlCreated = True

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def ApplyCaptionStyle(self, cbstyle=None, applyDefault=True):
        if cbstyle is None:
            cbstyle = fpb.EmptyCaptionBarStyle

        newstyle = cbstyle

        if applyDefault:
            if not newstyle.FirstColourUsed():
                newstyle.SetFirstColour(wx.WHITE)

            if not newstyle.SecondColourUsed():
                colour = self.GetParent().GetBackgroundColour()
                r, g, b = (
                    int(colour.Red()),
                    int(colour.Green()),
                    int(colour.Blue())
                )
                colour = ((r >> 1) + 20, (g >> 1) + 20, (b >> 1) + 20)
                newstyle.SetSecondColour(
                    wx.Colour(
                        colour[0],
                        colour[1],
                        colour[2])
                )

            if not newstyle.CaptionColourUsed():
                newstyle.SetCaptionColour(wx.BLACK)

            if not newstyle.CaptionFontUsed():
                newstyle.SetCaptionFont(self.GetParent().GetFont())

            if not newstyle.CaptionStyleUsed():
                newstyle.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_V)

        self._style = newstyle

    def SetCaptionStyle(self, cbstyle=None, applyDefault=True):
        if cbstyle is None:
            cbstyle = fpb.EmptyCaptionBarStyle

        self.ApplyCaptionStyle(cbstyle, applyDefault)
        self.Refresh()

    def GetCaptionStyle(self):
        return self._style

    def IsCollapsed(self):
        return self._collapsed

    def SetRightIndent(self, pixels):
        assert pixels >= 0
        self._rightIndent = pixels
        if self._foldIcons:
            self.Refresh()

    def Collapse(self):
        self._collapsed = True
        self.RedrawIconBitmap()

    def Expand(self):
        self._collapsed = False
        self.RedrawIconBitmap()

    def SetBoldFont(self):
        self.GetFont().SetWeight(wx.BOLD)

    def SetNormalFont(self):
        self.GetFont().SetWeight(wx.NORMAL)

    def IsVertical(self):
        fld = self.GetParent()
        if isinstance(fld, FoldPanelItem):
            return fld.IsVertical()
        else:
            raise Exception("ERROR: Wrong Parent " + repr(fld))

    def OnPaint(self, event):
        if not self._controlCreated:
            event.Skip()
            return

        dc = wx.PaintDC(self)
        wndRect = self.GetRect()
        vertical = self.IsVertical()

        self.FillCaptionBackground(dc)
        dc.SetFont(self._style.GetCaptionFont())
        dc.SetTextForeground(self._style.GetCaptionColour())

        if vertical:
            dc.DrawText(self._caption, 4, fpb.FPB_EXTRA_Y / 2)
        else:
            dc.DrawRotatedText(
                self._caption,
                fpb.FPB_EXTRA_Y / 2,
                wndRect.GetBottom() - 4,
                90
            )

        if self._foldIcons:

            index = self._collapsed

            if vertical:
                drw = wndRect.GetRight() - self._iconWidth - self._rightIndent
                self._foldIcons.Draw(
                    index,
                    dc,
                    drw,
                    (wndRect.GetHeight() - self._iconHeight) / 2,
                    wx.IMAGELIST_DRAW_TRANSPARENT
                )
            else:
                self._foldIcons.Draw(
                    index,
                    dc,
                    (wndRect.GetWidth() - self._iconWidth) / 2,
                    self._rightIndent,
                    wx.IMAGELIST_DRAW_TRANSPARENT
                )

    def FillCaptionBackground(self, dc):
        style = self._style.GetCaptionStyle()

        if style == fpb.CAPTIONBAR_GRADIENT_V:
            if self.IsVertical():
                self.DrawVerticalGradient(dc, self.GetRect())
            else:
                self.DrawHorizontalGradient(dc, self.GetRect())

        elif style == fpb.CAPTIONBAR_GRADIENT_H:
            if self.IsVertical():
                self.DrawHorizontalGradient(dc, self.GetRect())
            else:
                self.DrawVerticalGradient(dc, self.GetRect())

        elif style == fpb.CAPTIONBAR_SINGLE:
            self.DrawSingleColour(dc, self.GetRect())
        elif (
            style == fpb.CAPTIONBAR_RECTANGLE or
            style == fpb.CAPTIONBAR_FILLED_RECTANGLE
        ):
            self.DrawSingleRectangle(dc, self.GetRect())
        else:
            raise Exception(
                "STYLE Error: Undefined Style Selected: " + repr(style))

    def OnMouseEvent(self, event):
        send_event = False
        vertical = self.IsVertical()

        if event.LeftDown() and self._foldIcons:

            pt = event.GetPosition()
            rect = self.GetRect()

            drw = (rect.GetWidth() - self._iconWidth - self._rightIndent)
            if (
                vertical and
                pt.x > drw or
                not vertical and
                pt.y < (self._iconHeight + self._rightIndent)
            ):
                send_event = True

        elif event.LeftDClick():
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            send_event = True

        elif event.Entering() and self._foldIcons:
            pt = event.GetPosition()
            rect = self.GetRect()

            drw = (rect.GetWidth() - self._iconWidth - self._rightIndent)
            if (
                vertical and
                pt.x > drw or
                not vertical and
                pt.y < (self._iconHeight + self._rightIndent)
            ):
                self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            else:
                self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

        elif event.Leaving():
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

        elif event.Moving():
            pt = event.GetPosition()
            rect = self.GetRect()

            drw = (rect.GetWidth() - self._iconWidth - self._rightIndent)
            if (
                vertical and
                pt.x > drw or
                not vertical and
                pt.y < (self._iconHeight + self._rightIndent)
            ):
                self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            else:
                self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

        if send_event:
            event = fpb.CaptionBarEvent(fpb.wxEVT_CAPTIONBAR)
            event.SetId(self.GetId())
            event.SetEventObject(self)
            event.SetBar(self)
            self.GetEventHandler().ProcessEvent(event)

    def OnChar(self, event):
        event.Skip()

    def DoGetBestSize(self):
        if self.IsVertical():
            x, y = self.GetTextExtent(self._caption)
        else:
            y, x = self.GetTextExtent(self._caption)

        if x < self._iconWidth:
            x = self._iconWidth

        if y < self._iconHeight:
            y = self._iconHeight

        return wx.Size(x + fpb.FPB_EXTRA_X, y + fpb.FPB_EXTRA_Y)

    def DrawVerticalGradient(self, dc, rect):
        if rect.height < 1 or rect.width < 1:
            return

        dc.SetPen(wx.TRANSPARENT_PEN)
        col2 = self._style.GetSecondColour()
        col1 = self._style.GetFirstColour()

        r1, g1, b1 = int(col1.Red()), int(col1.Green()), int(col1.Blue())
        r2, g2, b2 = int(col2.Red()), int(col2.Green()), int(col2.Blue())

        flrect = float(rect.height)

        rstep = float((r2 - r1)) / flrect
        gstep = float((g2 - g1)) / flrect
        bstep = float((b2 - b1)) / flrect

        rf, gf, bf = 0, 0, 0

        for y in range(rect.y, rect.y + rect.height):
            currCol = (r1 + rf, g1 + gf, b1 + bf)

            dc.SetBrush(wx.Brush(currCol, wx.SOLID))
            dc.DrawRectangle(
                rect.x,
                rect.y + (y - rect.y),
                rect.width,
                rect.height
            )
            rf = rf + rstep
            gf = gf + gstep
            bf = bf + bstep

    def DrawHorizontalGradient(self, dc, rect):
        if rect.height < 1 or rect.width < 1:
            return

        dc.SetPen(wx.TRANSPARENT_PEN)

        col2 = self._style.GetSecondColour()
        col1 = self._style.GetFirstColour()

        r1, g1, b1 = int(col1.Red()), int(col1.Green()), int(col1.Blue())
        r2, g2, b2 = int(col2.Red()), int(col2.Green()), int(col2.Blue())

        flrect = float(rect.width)

        rstep = float((r2 - r1)) / flrect
        gstep = float((g2 - g1)) / flrect
        bstep = float((b2 - b1)) / flrect

        rf, gf, bf = 0, 0, 0

        for x in range(rect.x, rect.x + rect.width):
            currCol = (r1 + rf, g1 + gf, b1 + bf)

            dc.SetBrush(wx.Brush(currCol, wx.SOLID))
            dc.DrawRectangle(rect.x + (x - rect.x), rect.y, 1, rect.height)
            rf = rf + rstep
            gf = gf + gstep
            bf = bf + bstep

    def DrawSingleColour(self, dc, rect):
        if rect.height < 1 or rect.width < 1:
            return

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(self._style.GetFirstColour(), wx.SOLID))
        dc.DrawRectangle(rect.x, rect.y, rect.width, rect.height)

    def DrawSingleRectangle(self, dc, rect):
        if rect.height < 2 or rect.width < 1:
            return

        if self._style.GetCaptionStyle() == fpb.CAPTIONBAR_RECTANGLE:
            colour = self.GetParent().GetBackgroundColour()
            br = wx.Brush(colour, wx.SOLID)
        else:
            colour = self._style.GetFirstColour()
            br = wx.Brush(colour, wx.SOLID)

        pen = wx.Pen(self._style.GetSecondColour())
        dc.SetPen(pen)
        dc.SetBrush(br)
        dc.DrawRectangle(
            rect.x,
            rect.y,
            rect.width,
            rect.height - 1
        )

        bgpen = wx.Pen(self.GetParent().GetBackgroundColour())
        dc.SetPen(bgpen)
        dc.DrawLine(
            rect.x, rect.y + rect.height - 1,
            rect.x + rect.width,
            rect.y + rect.height - 1
        )

    def OnSize(self, event):
        if not self._controlCreated:
            event.Skip()
            return

        size = event.GetSize()

        if self._foldIcons:
            rect = wx.Rect(
                size.GetWidth() - self._iconWidth - self._rightIndent,
                0,
                self._iconWidth + self._rightIndent,
                self._iconWidth + self._rightIndent
            )
            diffX = size.GetWidth() - self._oldSize.GetWidth()

            if diffX > 1:
                rect.SetWidth(rect.GetWidth() + diffX + 10)
                rect.SetX(rect.GetX() - diffX - 10)

            self.RefreshRect(rect)

        else:

            rect = self.GetRect()
            self.RefreshRect(rect)

        self._oldSize = size

    def RedrawIconBitmap(self):
        if self._foldIcons:
            rect = self.GetRect()

            rect.SetX(rect.GetWidth() - self._iconWidth - self._rightIndent)
            rect.SetWidth(self._iconWidth + self._rightIndent)
            self.RefreshRect(rect)


def iter_child(parent, flag=True):
    try:
        for child in parent.GetChildren():
            child.Show(flag)
            iter_child(child, flag)
    except:
        pass


class FoldPanelItem(wx.Panel):

    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        caption="",
        foldIcons=None,
        collapsed=False,
        cbstyle=None,
        scrolled_panel=True
    ):
        wx.Panel.__init__(
            self,
            parent,
            id,
            wx.Point(0, 0),
            style=wx.CLIP_CHILDREN
        )

        self._controlCreated = False
        self._UserSize = 0
        self._PanelSize = 0
        self._LastInsertPos = 0
        self._itemPos = 0
        self._userSized = False

        if foldIcons is None:
            foldIcons = wx.ImageList(16, 16)

            bmp = fpb.ExpandedIcon.GetBitmap()
            foldIcons.Add(bmp)
            bmp = fpb.CollapsedIcon.GetBitmap()
            foldIcons.Add(bmp)

        self._foldIcons = foldIcons
        if cbstyle is None:
            cbstyle = fpb.EmptyCaptionBarStyle

        self._captionBar = CaptionBar(
            self,
            wx.ID_ANY,
            wx.Point(0, 0),
            size=wx.DefaultSize,
            caption=caption,
            foldIcons=foldIcons,
            cbstyle=cbstyle
        )

        if collapsed:
            self._captionBar.Collapse()
        self._controlCreated = True

        size = self._captionBar.GetSize()

        if self.IsVertical():
            if scrolled_panel:
                self.__panel = scrolled.ScrolledPanel(self, -1, style=wx.VSCROLL)
                self.__panel.SetupScrolling(scroll_x=False)
            else:
                self.__panel = wx.Panel(
                    self,
                    -1,
                    style=wx.BORDER_NONE
                )
            sizer = wx.BoxSizer(wx.VERTICAL)
            self.__main_sizer = wx.BoxSizer(wx.VERTICAL)
            self._PanelSize = size.GetHeight()
        else:
            if scrolled_panel:
                self.__panel = scrolled.ScrolledPanel(self, -1, style=wx.HSCROLL)
                self.__panel.SetupScrolling(scroll_y=False)
            else:
                self.__panel = wx.Panel(
                    self,
                    -1,
                    style=wx.BORDER_NONE
                )
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.__main_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self._PanelSize = size.GetWidth()

        sizer.Add(self._captionBar, 0, wx.EXPAND)
        sizer.Add(self.__panel, 1, wx.EXPAND)
        wx.Panel.SetSizer(self, sizer)
        self.__panel.SetSizer(self.__main_sizer)

        self._LastInsertPos = self._PanelSize
        self._items = []

        self.Bind(fpb.EVT_CAPTIONBAR, self.OnPressCaption)

        if collapsed:
            self.Collapse()
        else:
            self.Expand()

        self.Bind(wx.EVT_SIZE, self.OnSize)

    def SetSizer(self, sizer):
        self.__panel.SetSizer(sizer)

    def SetSizerAndFit(self, sizer):
        self.__panel.SetSizerAndFit(sizer)

    def OnSize(self, event):
        size = event.GetSize()
        caption_size = self._captionBar.GetSize()
        vsize = self.__panel.GetVirtualSize()

        if self._captionBar.IsCollapsed():
            size = caption_size

        else:
            size = (
                size[0] - caption_size[0] - 40,
                size[1] - caption_size[1] - 40
            )

        if self.IsVertical():
            self.__panel.SetVirtualSize((size[0], vsize[1]))
        else:
            self.__panel.SetVirtualSize((vsize[0], size[1]))

        event.Skip()

    def AddWindow(
        self,
        window,
        flags=fpb.FPB_ALIGN_WIDTH,
        spacing=fpb.FPB_DEFAULT_SPACING,
        leftSpacing=fpb.FPB_DEFAULT_LEFTSPACING,
        rightSpacing=fpb.FPB_DEFAULT_RIGHTSPACING
    ):
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)

        if flags | fpb.FPB_ALIGN_WIDTH == flags:
            sizer1.AddStretchSpacer(1)

        sizer2.Add(window, 1, wx.EXPAND | wx.LEFT, leftSpacing)
        sizer1.Add(sizer2, 1, wx.EXPAND | wx.ALL, spacing)

        sizer1.AddStretchSpacer(1)
        self.__main_sizer.Add(sizer1, wx.EXPAND | wx.RIGHT, rightSpacing)

    def AddSeparator(
        self,
        colour=wx.BLACK,
        spacing=fpb.FPB_DEFAULT_SPACING,
        leftSpacing=fpb.FPB_DEFAULT_LEFTSPACING,
        rightSpacing=fpb.FPB_DEFAULT_RIGHTSPACING
    ):
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)

        if self.IsVertical():
            line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
        else:
            line = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)

        sizer2.Add(line, 1, wx.EXPAND | wx.LEFT, leftSpacing)
        sizer1.Add(sizer2, 1, wx.EXPAND | wx.ALL, spacing)

        self.__main_sizer.Add(sizer1, wx.EXPAND | wx.RIGHT, rightSpacing)

    def Reposition(self, pos):
        return self.GetPanelLength()

    def OnPressCaption(self, event):
        event.SetTag(self)
        event.Skip()

    def ResizePanel(self):
        self.Layout()
        self.Refresh()
        self.Update()

    def IsVertical(self):
        if isinstance(self.GetParent(), FoldPanelBar):
            return self.GetParent().IsVertical()
        else:
            raise Exception(
                "ERROR: Wrong Parent " + repr(
                    self.GetParent())
            )

    def IsExpanded(self):
        return not self._captionBar.IsCollapsed()

    def Collapse(self):
        for child in self.GetChildren():
            if child not in (self.__panel, self._captionBar):
                child.Reparent(self.__panel)
                child.Show()
                iter_child(child)

        self._captionBar.Collapse()
        self.__panel.Hide()

    def Expand(self):
        self.__panel.Show()
        for child in self.GetChildren():
            if child not in (self.__panel, self._captionBar):
                child.Reparent(self.__panel)
                child.Show()
                iter_child(child)

        self._captionBar.Expand()

    def GetPanelLength(self):
        if self._captionBar.IsCollapsed():
            return self.GetCaptionLength()

        if self.IsVertical():
            return self.GetSize()[1]

        return self.GetSize()[0]

    def GetCaptionLength(self):
        size = self._captionBar.GetSize()
        return (
            self.IsVertical() and [size.GetHeight()] or [size.GetWidth()]
        )[0]

    def ApplyCaptionStyle(self, cbstyle):
        self._captionBar.SetCaptionStyle(cbstyle)

    def GetCaptionStyle(self):
        return self._captionBar.GetCaptionStyle()

    def SetCaptionLabel(self, label):
        self._captionBar._caption = label
        self._captionBar.Refresh()
        self._captionBar.Update()

    def GetCaptionLabel(self):
        return self._captionBar._caption


_fold_panel_window = fpb.FoldWindowItem


class FoldWindowItem(_fold_panel_window):

    def ResizeItem(self, size, vertical=True):
        pass

    def GetWindowLength(self, vertical=True):
        return self._spacing


fpb.FoldWindowItem = FoldWindowItem


class FoldPanelBar(wx.Panel):

    def __init__(
        self,
        parent,
        id=-1,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.TAB_TRAVERSAL | wx.NO_BORDER,
        agwStyle=0
    ):

        self._controlCreated = False

        if not agwStyle & (fpb.FPB_HORIZONTAL | fpb.FPB_VERTICAL):
            agwStyle = agwStyle | fpb.FPB_VERTICAL

        if agwStyle & fpb.FPB_HORIZONTAL:
            self._isVertical = False
            sizer = wx.BoxSizer(wx.HORIZONTAL)
        else:
            self._isVertical = True
            sizer = wx.BoxSizer(wx.VERTICAL)

        self._agwStyle = agwStyle

        wx.Panel.__init__(self, parent, id, pos, size, style)
        self.SetSizer(sizer)

        self._controlCreated = True
        self._panels = []

        self.Bind(fpb.EVT_CAPTIONBAR, self.OnPressCaption)

    def AddFoldPanel(
        self,
        caption="",
        collapsed=False,
        foldIcons=None,
        cbstyle=None,
        scrolled_panel=True
    ):

        self.Freeze()

        if cbstyle is None:
            cbstyle = fpb.EmptyCaptionBarStyle

        if foldIcons is None:
            foldIcons = wx.ImageList(16, 16)

            bmp = fpb.ExpandedIcon.GetBitmap()
            foldIcons.Add(bmp)
            bmp = fpb.CollapsedIcon.GetBitmap()
            foldIcons.Add(bmp)

        item = FoldPanelItem(
            self,
            -1,
            caption=caption,
            foldIcons=foldIcons,
            collapsed=collapsed,
            cbstyle=cbstyle,
            scrolled_panel=scrolled_panel
        )

        sizer = self.GetSizer()
        sizer.Add(item, 1, wx.EXPAND)

        if not collapsed:
            if (
                self._agwStyle & fpb.FPB_SINGLE_FOLD or
                self._agwStyle & fpb.FPB_EXCLUSIVE_FOLD
            ):
                for panel in self._panels:
                    panel.Collapse()

            if self._agwStyle & fpb.FPB_EXCLUSIVE_FOLD:
                self._panels.append(item)
                self.SetSizer(sizer)
                self.RepositionCollapsedToBottom()

        if collapsed and self._agwStyle & fpb.FPB_EXCLUSIVE_FOLD:
            self._panels.append(item)
            self.SetSizer(sizer)
            self.RepositionCollapsedToBottom()

        if item not in self._panels:
            self._panels.append(item)
            self.SetSizer(sizer)

        self.Layout()
        self.Refresh()
        self.Update()

        self.Thaw()

        return item

    def AddFoldPanelWindow(
        self,
        panel,
        window,
        flags=fpb.FPB_ALIGN_WIDTH,
        spacing=fpb.FPB_DEFAULT_SPACING,
        leftSpacing=fpb.FPB_DEFAULT_LEFTLINESPACING,
        rightSpacing=fpb.FPB_DEFAULT_RIGHTLINESPACING
    ):
        try:
            item = self._panels.index(panel)
        except:
            raise Exception(
                "ERROR: Invalid Panel Passed "
                "To AddFoldPanelWindow: " + repr(panel)
            )

        panel.AddWindow(window, flags, spacing, leftSpacing, rightSpacing)
        return 0

    def AddFoldPanelSeparator(
        self,
        panel,
        colour=wx.BLACK,
        spacing=fpb.FPB_DEFAULT_SPACING,
        leftSpacing=fpb.FPB_DEFAULT_LEFTLINESPACING,
        rightSpacing=fpb.FPB_DEFAULT_RIGHTLINESPACING
    ):
        try:
            item = self._panels.index(panel)
        except:
            raise Exception(
                "ERROR: Invalid Panel Passed To "
                "AddFoldPanelSeparator: " + repr(Panel)
            )

        panel.AddSeparator(colour, spacing, leftSpacing, rightSpacing)
        return 0

    def OnPressCaption(self, event):
        if event.GetFoldStatus():
            self.Collapse(event.GetTag())
        else:
            self.Expand(event.GetTag())

    def RefreshPanelsFrom(self, item):
        try:
            index = self._panels.index(item)
        except:
            raise Exception(
                "ERROR: Invalid Panel Passed To "
                "RefreshPanelsFrom: " + repr(item)
            )

        self.Freeze()
        for i in range(index, len(self._panels)):
            self._panels[i].Refresh()
            self._panels[i].Update()

        self.Thaw()

    def RedisplayFoldPanelItems(self):
        self.Layout()
        self.Refresh()
        self.Update()

    def RepositionCollapsedToBottom(self):
        self.Freeze()
        sizer = self.GetSizer()

        for panel in self._panels:
            sizer.Detach(panel)

        if self.IsVertical():
            sizer = wx.BoxSizer(wx.VERTICAL)
        else:
            sizer = wx.BoxSizer(wx.HORIZONTAL)

        for panel in self._panels:
            if panel.IsExpanded():
                sizer.Add(panel, 1, wx.EXPAND)
                break
        else:
            sizer.AddStretchSpacer(1)

        for panel in self._panels:
            if not panel.IsExpanded():
                sizer.Add(panel, 0, wx.EXPAND)

        self.SetSizer(sizer)
        self.Thaw()

    def GetPanelsLength(self, collapsed, expanded):
        value = 0
        for j in range(0, len(self._panels)):
            offset = self._panels[j].GetPanelLength()
            value = value + offset
            if self._panels[j].IsExpanded():
                expanded = expanded + offset
            else:
                collapsed = collapsed + offset

        return collapsed, expanded, value

    def Collapse(self, foldpanel):
        try:
            item = self._panels.index(foldpanel)
        except:
            raise Exception(
                "ERROR: Invalid Panel Passed To Collapse: " + repr(foldpanel))

        self.Freeze()

        foldpanel.Collapse()
        if self._agwStyle & fpb.FPB_EXCLUSIVE_FOLD:
            self.RepositionCollapsedToBottom()

        self.Layout()
        self.Refresh()
        self.Update()

        self.Thaw()

    def Expand(self, foldpanel):

        self.Freeze()
        if (
            self._agwStyle & fpb.FPB_SINGLE_FOLD or
            self._agwStyle & fpb.FPB_EXCLUSIVE_FOLD
        ):
            for panel in self._panels:
                panel.Collapse()

        foldpanel.Expand()

        if self._agwStyle & fpb.FPB_EXCLUSIVE_FOLD:
            self.RepositionCollapsedToBottom()
        self.Layout()
        self.Refresh()
        self.Update()

        self.Thaw()

    def ApplyCaptionStyle(self, foldpanel, cbstyle):
        foldpanel.ApplyCaptionStyle(cbstyle)

    def ApplyCaptionStyleAll(self, cbstyle):
        for panels in self._panels:
            self.ApplyCaptionStyle(panels, cbstyle)

    def GetCaptionStyle(self, foldpanel):
        return foldpanel.GetCaptionStyle()

    def IsVertical(self):
        return self._isVertical

    def GetFoldPanel(self, item):
        try:
            ind = self._panels[item]
            return self._panels[item]
        except:
            raise Exception(
                "ERROR: List Index Out Of Range Or Bad Item Passed: " +
                repr(item) +
                ". Item Should Be An Integer Between " +
                repr(0) +
                " And " +
                repr(len(self._panels))
            )

    def GetCount(self):
        try:
            return len(self._panels)
        except:
            raise Exception("ERROR: No Panels Have Been Added To FoldPanelBar")


class DayPanel(wx.Panel):

    def __init__(self, parent, *args):
        wx.Panel.__init__(self, parent)

        labels = [
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
        ]

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        ctrls = []
        sts = []

        for i, arg in enumerate(args):
            ctrl = wx.CheckBox(self, -1, '')
            ctrl.SetValue(arg)
            st = wx.StaticText(self, -1, labels[i])
            ctrls.append(ctrl)
            sts.append(st)

            sizer1 = wx.BoxSizer(wx.VERTICAL)
            sizer2 = wx.BoxSizer(wx.HORIZONTAL)

            sizer1.Add(st, 0, wx.ALIGN_CENTER_HORIZONTAL)

            sizer2.AddStretchSpacer(1)
            sizer2.Add(ctrl, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 5)
            sizer2.AddStretchSpacer(1)

            sizer1.Add(sizer2, 1)
            sizer.Add(sizer1, 0, wx.ALL, 5)

        eg.EqualizeWidths(tuple(sts))
        self.SetSizer(sizer)

        def get_value():
            return list(c.GetValue() for c in ctrls)

        def set_value(*values):
            for index, value in enumerate(values):
                ctrls[i].SetValue(value)

        self.GetValue = get_value
        self.SetValue  = set_value



class ScheduleSizer(wx.BoxSizer):

    def __init__(self, fold_panel, rule):
        wx.BoxSizer.__init__(self, wx.VERTICAL)

        def h_sizer(st, ctrl):
            szr = wx.BoxSizer(wx.HORIZONTAL)
            szr.Add(st, 0, wx.EXPAND | wx.ALL, 5)
            szr.Add(ctrl, 0, wx.EXPAND | wx.ALL, 5)
            return szr

        name_st = wx.StaticText(fold_panel, -1, 'Name:')
        name_ctrl = wx.TextCtrl(fold_panel, -1, rule.name)
        name_sizer = h_sizer(name_st, name_ctrl)

        enable_st = wx.StaticText(fold_panel, -1, 'Enable:')
        enable_ctrl = wx.CheckBox(fold_panel, -1, '')
        enable_ctrl.SetValue(bool(rule.enabled))
        enable_sizer = h_sizer(enable_st, enable_ctrl)

        top_sizer = h_sizer(name_sizer, enable_sizer)

        day_ctrl = DayPanel(
            fold_panel,
            rule.sunday,
            rule.monday,
            rule.tuesday,
            rule.wednesday,
            rule.thursday,
            rule.friday,
            rule.saturday
        )

        start_time_st = wx.StaticText(fold_panel, -1, 'Start Time:')
        start_time_spin = wx.SpinButton(
            fold_panel,
            -1,
            style=wx.SP_HORIZONTAL
        )

        start_time_ctrl = timectrl.TimeCtrl(
            fold_panel,
            -1,
            str(datetime.timedelta(seconds=rule.start_time)),
            fmt24hr=True,
            spinButton=start_time_spin
        )

        start_time_sizer = wx.BoxSizer(wx.VERTICAL)

        start_time_sizer.Add(start_time_ctrl)
        start_time_sizer.Add(start_time_spin)
        start_time_sizer = h_sizer(start_time_st, start_time_sizer)

        end_time_st = wx.StaticText(
            fold_panel,
            -1,
            'End Time:'
        )
        end_time_spin = wx.SpinButton(
            fold_panel,
            -1,
            style=wx.SP_HORIZONTAL
        )
        end_time_ctrl = timectrl.TimeCtrl(
            fold_panel,
            -1,
            str(datetime.timedelta(seconds=rule.end_time)),
            fmt24hr=True,
            spinButton=end_time_spin
        )

        end_time_sizer = wx.BoxSizer(wx.VERTICAL)
        end_time_sizer.Add(end_time_ctrl)
        end_time_sizer.Add(end_time_spin)
        end_time_sizer = h_sizer(end_time_st, end_time_sizer)

        event_top_sizer = wx.BoxSizer(wx.VERTICAL)
        event_top_sizer.Add(start_time_sizer)

        event_bottom_sizer = wx.BoxSizer(wx.VERTICAL)
        event_bottom_sizer.Add(end_time_sizer)

        event_right_sizer = wx.BoxSizer(wx.VERTICAL)
        event_right_sizer.Add(event_top_sizer)
        event_right_sizer.Add(event_bottom_sizer)

        calendar_ctrl = calendar.CalendarCtrl(
            fold_panel,
            -1,
            wx.DateTime().Set(
                day=rule.day,
                month=rule.month - 1,
                year=rule.year,
            ),
            style=(
                calendar.CAL_SUNDAY_FIRST |
                calendar.CAL_SHOW_HOLIDAYS |
                calendar.CAL_SEQUENTIAL_MONTH_SELECTION
            ),
        )

        event_sizer = h_sizer(calendar_ctrl, event_right_sizer)

        repeat_st = wx.StaticText(fold_panel, -1, 'Repeat:')
        repeat_ctrl = wx.Choice(
            fold_panel,
            -1,
            choices=['test1', 'test2', 'test3', 'test4']
        )
        repeat_ctrl.SetSelection(rule.repeat)

        repeat_sizer = h_sizer(repeat_st, repeat_ctrl)

        def save():
            rule.name = name_ctrl.GetValue()
            rule.enabled = int(enable_ctrl.GetValue())
            (
                rule.sunday,
                rule.monday,
                rule.tuesday,
                rule.wednesday,
                rule.thursday,
                rule.friday,
                rule.saturday
            ) = day_ctrl.GetValue()

            date = calendar_ctrl.GetDate()

            rule.day = date.Day
            rule.month = date.Month + 1
            rule.year = date.Year

            start_time = start_time_ctrl.GetValue().split(':')
            start_time = datetime.timedelta(
                hours=int(start_time[0]),
                minutes=int(start_time[1]),
                seconds=int(start_time[2])
            )

            rule.start_time = start_time.seconds

            end_time = end_time_ctrl.GetValue().split(':')
            end_time = datetime.timedelta(
                hours=int(end_time[0]),
                minutes=int(end_time[1]),
                seconds=int(end_time[2])
            )
            rule.end_time = end_time.seconds
            rule.repeat = repeat_ctrl.GetSelection()

        def reset():
            name_ctrl.SetValue(rule.name)
            enable_ctrl.SetValue(bool(rule.enabled))
            day_ctrl.SetValue(
                rule.sunday,
                rule.monday,
                rule.tuesday,
                rule.wednesday,
                rule.thursday,
                rule.friday,
                rule.saturday
            )
            calendar_ctrl.SetDate(
                wx.DateTime().Set(
                    day=rule.day,
                    month=rule.month - 1,
                    year=rule.year,
                )
            )
            start_time_ctrl.SetValue(
                str(datetime.timedelta(seconds=rule.start_time))
            )
            end_time_ctrl.SetValue(
                str(datetime.timedelta(seconds=rule.end_time))
            )
            repeat_ctrl.SetSelection(rule.repeat)

        if isinstance(fold_panel.GetGrandParent(), ScheduleFoldPanel):
            start_action = rule.start_action
            start_choices = ['Off', 'On']
            if start_action == -1:
                start_action = 2
                start_choices += ['Unknown']

            start_action_st = wx.StaticText(fold_panel, -1, 'Start Action:')
            start_action_ctrl = wx.Choice(
                fold_panel,
                -1,
                choices=start_choices
            )

            start_action_ctrl.SetSelection(start_action)
            start_action_sizer = h_sizer(start_action_st, start_action_ctrl)

            end_choices = ['Off', 'On']
            end_action = rule.end_action
            if end_action is None:
                end_action = 2
                end_choices += ['Unknown']

            end_action_st = wx.StaticText(fold_panel, -1, 'End Action:')
            end_action_ctrl = wx.Choice(
                fold_panel,
                -1,
                choices=end_choices
            )

            print 'end_action', end_action

            end_action_ctrl.SetSelection(end_action)
            end_action_sizer = h_sizer(end_action_st, end_action_ctrl)
            event_top_sizer.Add(start_action_sizer)
            event_bottom_sizer.Add(end_action_sizer)

            def on_save(_):
                save()
                rule.start_action = start_action_ctrl.GetSelection()
                rule.end_action = end_action_ctrl.GetSelection()
                rule.save()

            def on_cancel(_):
                reset()
                start_action_ctrl.SetSelection(start_action)
                end_action_ctrl.SetSelection(end_action)

        else:
            frequency_st = wx.StaticText(fold_panel, -1, 'Frequency:')
            frequency_ctrl = eg.SpinIntCtrl(fold_panel, -1, rule.frequency)
            frequency_sizer = h_sizer(frequency_st, frequency_ctrl)

            duration_st = wx.StaticText(fold_panel, -1, 'Duration:')
            duration_ctrl = eg.SpinIntCtrl(fold_panel, -1, rule.duration)
            duration_sizer = h_sizer(duration_st, duration_ctrl)

            lastfor_st = wx.StaticText(fold_panel, -1, 'Lasts For:')
            lastfor_ctrl = eg.SpinIntCtrl(fold_panel, -1, rule.lastfor)
            lastfor_sizer = h_sizer(lastfor_st, lastfor_ctrl)

            antitheft_sizer = wx.BoxSizer(wx.VERTICAL)
            antitheft_sizer.Add(frequency_sizer)
            antitheft_sizer.Add(duration_sizer)
            antitheft_sizer.Add(lastfor_sizer)
            event_sizer.Add(antitheft_sizer)

            def on_save(_):
                save()
                rule.frequency = frequency_ctrl.GetValue()
                rule.duration = duration_ctrl.GetValue()
                rule.lastfor = lastfor_ctrl.GetValue()
                rule.save()

            def on_cancel(_):
                reset()
                frequency_ctrl.SetValue(rule.frequency)
                duration_ctrl.SetValue(rule.duration)
                lastfor_ctrl.SetValue(rule.lastfor)

        save_button = wx.Button(fold_panel, wx.ID_SAVE, size=(40, 25))
        cancel_button = wx.Button(fold_panel, wx.ID_CANCEL, size=(40, 25))

        save_button.Bind(wx.EVT_BUTTON, on_save)
        cancel_button.Bind(wx.EVT_BUTTON, on_cancel)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.AddStretchSpacer(1)
        button_sizer.Add(save_button, 0, wx.RIGHT, 20)
        button_sizer.Add(cancel_button)
        button_sizer.AddStretchSpacer(1)

        self.Add(top_sizer)
        self.Add(day_ctrl)
        self.Add(event_sizer)
        self.Add(repeat_sizer)
        self.Add(button_sizer)


class ScheduleFoldPanel(wx.Panel):

    def __init__(self, parent, device):
        wx.Panel.__init__(self, parent, -1)

        fold_panel_bar = FoldPanelBar(
            self,
            -1,
            size=(450, 500),
            agwStyle=(
                fpb.FPB_VERTICAL | fpb.FPB_EXCLUSIVE_FOLD
            )
        )

        for rule in device.schedule:
            fold_panel = fold_panel_bar.AddFoldPanel(
                '{0} ({1})'.format(rule.name, rule.id),
                collapsed=True,
                foldIcons=IMAGE_LIST,
                scrolled_panel=False
            )

            sizer = ScheduleSizer(fold_panel, rule)
            fold_panel.SetSizer(sizer)
            fold_panel.Show(False)

        button = wx.Button(self, -1, 'New Schedule')
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.AddStretchSpacer(1)
        button_sizer.Add(button, 0, wx.RIGHT, 5)

        def on_button(_):
            rule = device.schedule.create()
            fold_panel = fold_panel_bar.AddFoldPanel(
                'New_Schedule'.format(rule.name, rule.id),
                collapsed=False,
                foldIcons=IMAGE_LIST
            )

            sizer = ScheduleSizer(fold_panel, rule)
            fold_panel.SetSizer(sizer)

        button.Bind(wx.EVT_BUTTON, on_button)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(fold_panel_bar, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(button_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)


class AntiTheftFoldPanel(wx.Panel):

    def Show(self, flag=True):

        for child in self.GetChildren():
            child.Show(flag)

        wx.Panel.Show(self, flag)

    def Hide(self, flag=True):
        self.Show(not flag)

    def __init__(self, parent, device):
        wx.Panel.__init__(self, parent, -1)

        fold_panel_bar = FoldPanelBar(
            self,
            -1,
            size=(450, 500),
            agwStyle=(
                fpb.FPB_VERTICAL | fpb.FPB_EXCLUSIVE_FOLD
            )
        )

        for rule in device.antitheft:

            fold_panel = fold_panel_bar.AddFoldPanel(
                '{0} ({1})'.format(rule.name, rule.id),
                collapsed=True,
                foldIcons=IMAGE_LIST,
                scrolled_panel=False
            )

            sizer = ScheduleSizer(fold_panel, rule)
            fold_panel.SetSizer(sizer)

        button = wx.Button(self, -1, 'New Anti Theft')
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.AddStretchSpacer(1)
        button_sizer.Add(button, 0, wx.RIGHT, 5)

        def on_button(_):
            rule = device.schedule.create()
            fold_panel = fold_panel_bar.AddFoldPanel(
                'New_Schedule'.format(rule.name, rule.id),
                collapsed=False,
                foldIcons=IMAGE_LIST
            )

            sizer = ScheduleSizer(fold_panel, rule)
            fold_panel.SetSizer(sizer)

        button.Bind(wx.EVT_BUTTON, on_button)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(fold_panel_bar, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(button_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)


class FoldPanels(FoldPanelBar):

    def __init__(self, parent, device):
        FoldPanelBar.__init__(
            self,
            parent,
            -1,
            size=(450, 500),
            agwStyle=(
                fpb.FPB_VERTICAL | fpb.FPB_EXCLUSIVE_FOLD
            )
        )

        schedule_panel = self.AddFoldPanel(
            'Schedule',
            collapsed=True,
            foldIcons=IMAGE_LIST
        )
        schedule_fold_panel = ScheduleFoldPanel(schedule_panel, device)
        schedule_sizer = wx.BoxSizer(wx.VERTICAL)
        schedule_sizer.Add(schedule_fold_panel, 1, wx.EXPAND)
        schedule_panel.SetSizer(schedule_sizer)

        antitheft_panel = self.AddFoldPanel(
            'Anti Theft',
            collapsed=True,
            foldIcons=IMAGE_LIST
        )
        antitheft_fold_panel = AntiTheftFoldPanel(antitheft_panel, device)
        antitheft_sizer = wx.BoxSizer(wx.VERTICAL)
        antitheft_sizer.Add(antitheft_fold_panel, 1, wx.EXPAND)
        antitheft_panel.SetSizer(antitheft_sizer)

        countdown_panel = self.AddFoldPanel(
            'Count Down',
            collapsed=True,
            foldIcons=IMAGE_LIST
        )
        countdown_sizer = wx.BoxSizer(wx.VERTICAL)

        def h_sizer(st1, ctrl1, st2, ctrl2):
            szr = wx.BoxSizer(wx.HORIZONTAL)
            szr.Add(st1, 0, wx.EXPAND | wx.ALL, 5)
            szr.Add(ctrl1, 0, wx.EXPAND | wx.ALL, 5)
            szr.Add(st2, 0, wx.EXPAND | wx.ALL, 5)
            szr.Add(ctrl2, 0, wx.EXPAND | wx.ALL, 5)
            countdown_sizer.Add(szr, 0, wx.EXPAND)

        for rule in device.countdown:
            name_st = wx.StaticText(countdown_panel, -1, 'Name:')
            name_ctrl = wx.TextCtrl(countdown_panel, -1, rule.name)

            enabled_st = wx.StaticText(countdown_panel, -1, 'Enabled:')
            enabled_ctrl = wx.CheckBox(countdown_panel, -1, '')
            enabled_ctrl.SetValue(rule.enabled)

            h_sizer(name_st, name_ctrl, enabled_st, enabled_ctrl)

            delay_st = wx.StaticText(countdown_panel, -1, 'Delay:')
            delay_ctrl = eg.SpinIntCtrl(countdown_panel, -1, rule.delay)

            action_st = wx.StaticText(countdown_panel, -1, 'Action:')
            action_ctrl = wx.Choice(
                countdown_panel,
                -1,
                choices=['Off', 'On']
            )
            action_ctrl.SetSelection(rule.action)
            h_sizer(delay_st, delay_ctrl, action_st, action_ctrl)

        countdown_panel.SetSizer(countdown_sizer)


class DeviceFoldPanel(FoldPanelBar):

    def __init__(self, parent):
        FoldPanelBar.__init__(
            self,
            parent,
            -1,
            size=(450, 500),
            agwStyle=(
                fpb.FPB_VERTICAL | fpb.FPB_EXCLUSIVE_FOLD
            )
        )

        for device in tp_link:

            fold_panel = self.AddFoldPanel(
                '{0} ({1})'.format(device.alias, device.id),
                collapsed=True,
                foldIcons=IMAGE_LIST,
                scrolled_panel=False
            )
            device_panel = FoldPanels(fold_panel, device)
            device_sizer = wx.BoxSizer(wx.VERTICAL)
            device_sizer.Add(device_panel, 1, wx.EXPAND)
            fold_panel.SetSizer(device_sizer)
            iter_child(device_panel, False)
