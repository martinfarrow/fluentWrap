class fluentWrap():
    """Wrapper class to create iterable objects from collections
       of list, dicts and other iterables"""

    is_attribute = re.compile('^[^_]')

    def __init__(self, item, raiseOnMissing=False):

        self.__raiseOnMissing = raiseOnMissing

        # item has to be iterable

        try:
            iter(item)
        except TypeError:
            raise TypeError("Item is not iterable")

        if (isinstance(item, list)):
            newitem = list()
            for part in item:
                if isinstance(part, (dict, list)):
                    newitem.append(fluentWrap(part))
                else:
                    newitem.append(item)
            self.__list = newitem
        else:
            for part in item:
                cand = item[part]
                if (isinstance(cand, (dict, list))):
                    result = fluentWrap(cand)
                else:
                    result = cand
                self.__dict__[part] = result


    def __add__(self, other):
        """Plus operator overload"""

        if not isinstance(other, fluentWrap):
            other = fluentWrap(other)

        for item in other.__dict__:

            # if parts are them same name and both fluentWraps then
            # add them, otherwise just overwrite self with whatever
            # is in other if item already exists in self

            if fluentWrap.is_attribute.match(item):
                if item in self.__dict__:
                    if (isinstance(self.__dict__[item], fluentWrap) and
                        isinstance(other.__dict__[item], fluentWrap)):
                           self.__dict__[item] = self.__dict__[item] + other.__dict__[item]
                    else:
                        self.__dict__[item] = other.__dict__[item]
                else:
                    self.__dict__[item] = other.__dict__[item]

        # encased lists either get created or appended

        if '_fluentWrap__list' in other.__dict__:
            if not '_fluentWrap__list' in self.__dict__:
                self._fluentWrap__list = list()
            self._fluentWrap__list.extend(other.__dict__['_fluentWrap__list'])
        return self

    def __getattr__(self, item):
        if self.__raiseOnMissing:
            raise AttributeError("No such item({})".format(item))
            return 
        else:
            return None

    def __iter__(self):
       return fluentIter(self) 

    def __str__(self):
        """Human readable string representation of object - note with recursion"""
        ret="FluentObject("
        comma=""
        for item in self.__dict__:
            if fluentWrap.is_attribute.match(item):
                ret+="{}{}={}".format(comma, item, str(self.__dict__[item]))
                comma=", "
        if '_fluentWrap__list' in self.__dict__:
            ret+="{}list(len={})".format(comma,len(self.__list))
        ret+=")"
        return ret

    def getKeys(self):
        """ Return the name of the all the keys in the top level object """
        return [ name for name in self.__dict__ if fluentWrap.isattrib.match(name) ]

    def getKey(self, key):
        """Return the named item"""
        if key in self.getKeys:
            return self.__dict__[key]
        else:
            raise AttributeError("Key ({}) does not exist".format(key))

    def get(self, position):
        """Return item in position from encased list"""

        if not isinstance(position, int):
            raise ValueError("Position must be an int")

        if position < 0:
            raise IndexError("Negitive indicies are not allowed")

        l = len(self.__dict__['_fluentWrap__list'])

        if '_fluentWrap__list' in self.__dict__:
            if position >= l:
                raise IndexError("Index out of range")
            else:
                return self.__dict__['_fluentWrap__list'][position]
        return None

    def len(self):
        """Return size of encased list"""
        if '_fluentWrap__list' in self.__dict__:
            return len(self.__dict__['_fluentWrap__list'])
        else:
            return 0

class fluentIter():

    def __init__(self, fluent):
        self.fluent = fluent
        self.items = list()
        self.counter = 0
        self.listmode = False
        for item in self.fluent.__dict__:
            if fluentWrap.is_attribute.match(item):
                self.items.append(item)
        self.items=sorted(self.items)

    def __next__(self):

        # normal item
        if self.counter < len(self.items):
            res = self.fluent.__dict__[self.items[self.counter]]
            self.counter += 1
            return res

        # turn on listmode after normal mode
        if self.listmode is False and '_fluentWrap__list' in self.fluent.__dict__:
            self.listmode = True
            self.listCounter = 0 
            self.listSize = len(self.fluent.__dict__['_fluentWrap__list'])

        # output the list
        if self.listmode and self.listCounter < self.listSize:
            res = self.fluent.__dict__['_fluentWrap__list'][self.listCounter]
            self.listCounter += 1
            return res

        # The End
        raise StopIteration
