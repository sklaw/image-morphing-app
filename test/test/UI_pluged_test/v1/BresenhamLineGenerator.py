import math

class BresenhamLineGenerator:
    def __init__(self, v1, v2):

        self.x1 = v1[0]
        self.y1 = v1[1]
        self.x2 = v2[0]
        self.y2 = v2[1]

        self.x = self.x1
        self.y = self.y1

        self.dx = self.x2-self.x1
        self.dy = self.y2-self.y1

        if self.dx > 0:
            self.signx = 1
        else:
            self.signx = -1
            self.dx = -self.dx

        if self.dy > 0:
            self.signy = 1
        else:
            self.signy = -1
            self.dy = -self.dy

        self.changed = False
        if self.dy > self.dx:
            tmp = self.dx
            self.dx = self.dy
            self.dy = tmp
            self.changed = True

        self.e = 2*self.dy-self.dx

        self.done = False

    def is_done(self):
        if self.x == self.x2 and self.y == self.y2:
            return True
        else:
            return False

    def get_next_point(self):
        return_x = self.x
        return_y = self.y

        if self.done:
            return None
        if return_x == self.x2 and return_y == self.y2:
            self.done = True
            return [return_x, return_y]

        if self.e >= 0:
            if (self.changed) :
                self.x += self.signx
            
            else :
                self.y += self.signy
            
            self.e = self.e-2*self.dx
        

        if (self.changed) :
            self.y += self.signy
        else :
            self.x += self.signx
        
        self.e = self.e+2*self.dy
        

        return [return_x, return_y]