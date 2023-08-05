import re
import curses.ascii
from enum import Enum

__all__ = ['SHAUNDecoder']

class ParseError(BaseException):
    def __init__(self, raw, col, msg):
        self.raw = raw
        self.col = col
        self.msg = msg

    def __str__(self):
        return 'parse error at line: %i column: %i "%s"' % (self.raw, self.col, self.msg)

    def __repr__(self):
        return str(self)

class TokenType(Enum):
    LBRACKET = 0
    RBRACKET = 1
    LHOOK = 2
    RHOOK = 3
    STR_LIT = 4
    NUM_LIT = 5
    BOOL_LIT = 6
    NULL_LIT = 7
    NAME = 8
    ATTRIB_SEP = 9

class Token(object):
    def __init__(self, t, v, raw, col):
        self.t = t
        self.v = v
        self.raw = raw
        self.col = col

    def __str__(self):
        if self.v != None:
            return str(self.v)
        else:
            return str(self.t)

    def __repr__(self):
        return str(self)

COMBEG = [ '/', '#', '(' ]
WSLIST = [ ' ', '\n', ',', '\t' ] + COMBEG
NUM_SYMS = [ '+', '-', '.', 'e', 'E' ]

class SHAUNDecoder(object):
    def __init__(self, buf, no_unit_single=None, numeric_ctor=None):

        if no_unit_single is None:
            self.no_unit_single = False
        else:
            self.no_unit_single = no_unit_single

        if numeric_ctor is None:
            self.numeric_ctor = lambda x, y: (x, y)
        else:
            self.numeric_ctor = numeric_ctor

        self.tokens = []
        self.ti = 0

        self.buf = buf
        self.i  = 0

        self.raw = 1
        self.col = 1


    def peek(self):
        return self.buf[self.i:self.i+1]

    def next(self):
        if self.peek() == '\n':
            self.raw = self.raw + 1
            self.col = 0
        else:
            self.col = self.col + 1
        self.i = self.i + 1
        return self.peek()

    def skipws(self):
        c = self.peek()
        while c in WSLIST:
            if c in COMBEG:
                self.skipcom()
            c = self.next()

    def skipcom(self):
        pass
                
    def lex(self):
        c = self.peek()
        while c != '':
            if curses.ascii.isalpha(c):
                self.lex_name()
            elif curses.ascii.isdigit(c) or c == '.' or c == '+' or c == '-':
                self.lex_numeric()
            elif c == '{':
                self.push_token(TokenType.LBRACKET, None)
                c = self.next()
            elif c == '}':
                self.push_token(TokenType.RBRACKET, None)
                c = self.next()
            elif c == '[':
                self.push_token(TokenType.LHOOK, None)
                c = self.next()
            elif c == ']':
                self.push_token(TokenType.RHOOK, None)
                c = self.next()
            elif c == ':':
                self.push_token(TokenType.ATTRIB_SEP, None)
                c = self.next()
            elif c == '"':
                self.lex_string()
            self.skipws()
            c = self.peek()

    def lex_name(self):
        c = self.peek()
        s = ''

        while curses.ascii.isalnum(c) or c == '_':
            s = s + c
            c = self.next()

        if s == 'true' or s == 'false':
            self.push_token(TokenType.BOOL_LIT, s == 'true')
        elif s == 'null':
            self.push_token(TokenType.NULL_LIT, None)
        else:
            self.push_token(TokenType.NAME, s)

    def lex_numeric(self):
        c = self.peek()
        snum = ''

        while curses.ascii.isdigit(c) or c in NUM_SYMS:
            snum = snum + c
            c = self.next()
        self.next()
        self.push_token(TokenType.NUM_LIT, float(snum))

    def lex_string(self):
        c = self.next()
        s = ''

        while c != '"':
            if c == '/':
                c = escape[self.next()]

            s = s + c
            c = self.next()

        self.next()
        self.push_token(TokenType.STR_LIT, s)

    def push_token(self, t, v):
        self.tokens.append(Token(t, v, self.raw, self.col))

    def tok(self):
        return self.tokens[self.ti]

    def ntok(self):
        self.ti = self.ti + 1
        return self.tok()

    def check_tt(self, tt, msg):
        if self.tok().t != tt:
            raise ParseError(self.tok().raw, self.tok().col, msg)

    def parse_object(self):
        self.check_tt(TokenType.LBRACKET, 'expected right bracket')

        obj = {}
        while self.ntok().t != TokenType.RBRACKET:
            name = self.parse_name()
            self.ntok()
            self.check_tt(TokenType.ATTRIB_SEP, 'expected attribute separator')
            self.ntok()
            val = self.parse_value()
            obj[name] = val

        return obj

    def parse_name(self):
        self.check_tt(TokenType.NAME, 'expected name')
        return self.tok().v

    def parse_value(self):
        fl = { TokenType.LBRACKET    : self.parse_object
                , TokenType.LHOOK    : self.parse_list
                , TokenType.STR_LIT  : self.parse_string
                , TokenType.NULL_LIT : self.parse_null
                , TokenType.BOOL_LIT : self.parse_bool
                , TokenType.NUM_LIT  : self.parse_numeric }

        for t, f in fl.items():
            if self.tok().t == t:
                return f()

        raise ParseError(self.tok().raw, self.tok().col, 'expected value')

    def parse_list(self):
        self.check_tt(TokenType.LHOOK, 'expected left hook')

        ret = []
        while self.ntok().t != TokenType.RHOOK:
            ret.append(self.parse_value())

        return ret

    def parse_string(self):
        self.check_tt(TokenType.STR_LIT, 'expected string litteral')
        return self.tok().v

    def parse_numeric(self):
        self.check_tt(TokenType.NUM_LIT, 'expected numeric litteral')
        val = self.tok().v
        unit = None
        if self.tokens[self.ti+1].t == TokenType.NAME and self.tokens[self.ti+2].t != TokenType.ATTRIB_SEP:
            unit = self.ntok().v
            return self.numeric_ctor(val, unit)

        if self.no_unit_single:
            return val
        else:
            return self.numeric_ctor(val, None)

    def parse_bool(self):
        self.check_tt(TokenType.BOOL_LIT, 'expected bool litteral')
        return self.tok().v

    def parse_null(self):
        self.check_tt(TokenType.NULL_LIT, 'expected null litteral')
        return None

    def parse(self):
        if self.tok().t == TokenType.LBRACKET:
            return self.parse_object()
        
        obj = {}
        while self.ntok().t != TokenType.RBRACKET:
            name = self.parse_name()
            self.ntok()
            self.check_tt(TokenType.ATTRIB_SEP, 'expected attribute separator')
            self.ntok()
            val = self.parse_value()
            obj[name] = val

        return obj


    def decode(self):
        self.lex()
        return self.parse()

