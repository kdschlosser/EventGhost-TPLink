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


def remap(val, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    return (
               ((val - old_min) * new_range) / old_range
           ) + new_min


class ColorChooser(wx.Panel):

    def __init__(
        self,
        parent,
        id=-1,
        value=(127, 127, 127),
        size=wx.DefaultSize,
        pos=wx.DefaultPosition,
        style=wx.BORDER_NONE
    ):
        wx.Panel.__init__(
            self,
            parent,
            id,
            style=style,
            pos=pos,
            size=size
        )
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.red = value[0]
        self.green = value[1]
        self.blue = value[2]
        self.red_capture = False
        self.green_capture = False
        self.blue_capture = False

        self.red_cursor = (0, 0, 0, 0, 5)
        self.green_cursor = (0, 0, 0, 0, 5)
        self.blue_cursor = (0, 0, 0, 0, 5)

        self.SetBackgroundColour(parent.GetBackgroundColour())

    def GetValue(self):
        return self.red, self.green, self.blue

    def OnSize(self, evt):
        def do():
            self.Refresh()
            self.Update()

        wx.CallAfter(do)

        evt.Skip()

    def OnLeave(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
            self.red_capture = False
            self.green_capture = False
            self.blue_capture = False
            self.Refresh()
            self.Update()
        evt.Skip()

    def OnLeftDown(self, evt):
        x, y = evt.GetPosition()

        red_start_x = self.red_cursor[0]
        red_start_y = self.red_cursor[1]
        red_stop_x = red_start_x + self.red_cursor[2]
        red_stop_y = red_start_y + self.red_cursor[3]

        green_start_x = self.green_cursor[0]
        green_start_y = self.green_cursor[1]
        green_stop_x = green_start_x + self.green_cursor[2]
        green_stop_y = green_start_y + self.green_cursor[3]

        blue_start_x = self.blue_cursor[0]
        blue_start_y = self.blue_cursor[1]
        blue_stop_x = blue_start_x + self.blue_cursor[2]
        blue_stop_y = blue_start_y + self.blue_cursor[3]

        if (
            red_start_x < x < red_stop_x and
            red_start_y < y < red_stop_y
        ):
            self.red_capture = True
        elif (
            green_start_x < x < green_stop_x and
            green_start_y < y < green_stop_y
        ):
            self.green_capture = True
        elif (
            blue_start_x < x < blue_stop_x and
            blue_start_y < y < blue_stop_y
        ):
            self.blue_capture = True

        if True in (self.red_capture, self.green_capture, self.blue_capture):
            self.CaptureMouse()

        evt.Skip()

    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
            self.red_capture = False
            self.green_capture = False
            self.blue_capture = False
            self.Refresh()
            self.Update()
        evt.Skip()

    def OnMotion(self, evt):
        if self.HasCapture():
            width = self.GetSizeTuple()[0]
            bar_width = width - 20

            x = evt.GetPosition()[0]

            def do():
                self.Refresh()
                self.Update()

            if self.red_capture:
                red = remap(x, 5, bar_width, 0, 255)
                if red < 0:
                    red = 0
                elif red > 255:
                    red = 255

                if red != self.red:
                    self.red = red
                    wx.CallAfter(do)
            elif self.green_capture:
                green = remap(x, 5, bar_width, 0, 255)
                if green < 0:
                    green = 0
                elif green > 255:
                    green = 255

                if green != self.green:
                    self.green = green
                    wx.CallAfter(do)
            elif self.blue_capture:
                blue = remap(x, 5, bar_width, 0, 255)
                if blue < 0:
                    blue = 0
                elif blue > 255:
                    blue = 255

                if blue != self.blue:
                    self.blue = blue
                    wx.CallAfter(do)
        evt.Skip()

    def OnPaint(self, evt):
        width, height = self.GetSizeTuple()
        width -= 10
        height -= 10
        bar_height = (height / 3) - 10
        back_colour = self.GetBackgroundColour()

        gc = wx.PaintDC(self)

        gc.SetBrush(wx.Brush(back_colour))
        gc.SetPen(wx.Pen(back_colour, 1))

        gc.Clear()
        gc.SetTextForeground(self.GetForegroundColour())
        gc.SetTextBackground(back_colour)

        font = self.GetFont()
        font.SetPixelSize(wx.Size(0, bar_height - (bar_height / 12)))
        gc.SetFont(font)

        text_w, text_h = gc.GetTextExtent('G')

        bar_width = width - 10 - text_w
        cursor_width = 13
        cursor_height = bar_height - 2
        cursor_half = cursor_width / 2

        red_cursor = remap(
            self.red,
            0,
            255,
            width - bar_width - 5,
            width - 8
        )
        green_cursor = remap(
            self.green,
            0,
            255,
            width - bar_width - 5,
            width - 8
        )
        blue_cursor = remap(
            self.blue,
            0,
            255,
            width - bar_width - 5,
            width - 8
        )

        red = wx.Rect(
            width - bar_width - 5,
            10,
            bar_width,
            bar_height
        )
        green = wx.Rect(
            width - bar_width - 5,
            20 + bar_height,
            bar_width,
            bar_height
        )
        blue = wx.Rect(
            width - bar_width - 5,
            30 + (bar_height * 2),
            bar_width, bar_height
        )

        cursor_line_height = int(bar_height * 0.6)
        cursor_line_start = ((bar_height - cursor_line_height) / 2) + 1

        red_cursor_line = (
            red_cursor,
            red.GetY() + cursor_line_start,
            red_cursor,
            red.GetY() + cursor_line_start + cursor_line_height
        )
        green_cursor_line = (
            green_cursor,
            green.GetY() + cursor_line_start,
            green_cursor,
            green.GetY() + cursor_line_start + cursor_line_height
        )
        blue_cursor_line = (
            blue_cursor,
            blue.GetY() + cursor_line_start,
            blue_cursor,
            blue.GetY() + cursor_line_start + cursor_line_height
        )

        red_fill = wx.Rect(
            red.GetX() + 1,
            red.GetY() + 2,
            red.GetWidth() - 2,
            red.GetHeight() - 2
        )
        green_fill = wx.Rect(
            green.GetX() + 1,
            green.GetY() + 2,
            green.GetWidth() - 2,
            green.GetHeight() - 2
        )
        blue_fill = wx.Rect(
            blue.GetX() + 1,
            blue.GetY() + 2,
            blue.GetWidth() - 2,
            blue.GetHeight() - 2
        )

        self.red_cursor = (
            red_cursor - cursor_half,
            red.GetY() + 2,
            cursor_width,
            cursor_height,
            2
        )
        self.green_cursor = (
            green_cursor - cursor_half,
            green.GetY() + 2,
            cursor_width,
            cursor_height,
            2
        )
        self.blue_cursor = (
            blue_cursor - cursor_half,
            blue.GetY() + 2,
            cursor_width,
            cursor_height,
            2
        )

        gc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 0), wx.BRUSHSTYLE_TRANSPARENT))
        gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))

        gc.DrawRectangle(
            red.GetX(),
            red.GetY() + 1,
            red.GetWidth(),
            red.GetHeight()
        )
        gc.DrawRectangle(
            green.GetX(),
            green.GetY() + 1,
            green.GetWidth(),
            green.GetHeight()
        )
        gc.DrawRectangle(
            blue.GetX(),
            blue.GetY() + 1,
            blue.GetWidth(),
            blue.GetHeight()
        )

        gc.GradientFillLinear(
            red_fill,
            wx.Colour(0, self.green, self.blue),
            wx.Colour(255, self.green, self.blue)
        )
        gc.GradientFillLinear(
            green_fill,
            wx.Colour(self.red, 0, self.blue),
            wx.Colour(self.red, 255, self.blue)
        )
        gc.GradientFillLinear(
            blue_fill,
            wx.Colour(self.red, self.green, 0),
            wx.Colour(self.red, self.green, 255)
        )

        gc.SetPen(wx.Pen(back_colour, 1))
        gc.DrawRoundedRectangle(*self.red_cursor)
        gc.DrawRoundedRectangle(*self.green_cursor)
        gc.DrawRoundedRectangle(*self.blue_cursor)
        gc.DrawLine(*red_cursor_line)
        gc.DrawLine(*green_cursor_line)
        gc.DrawLine(*blue_cursor_line)

        gc.DrawText('R', 4, red.GetY() - 1)
        gc.DrawText('G', 3, green.GetY() - 1)
        gc.DrawText('B', 4, blue.GetY() - 1)

    def OnEraseBackground(self, _):
        pass
