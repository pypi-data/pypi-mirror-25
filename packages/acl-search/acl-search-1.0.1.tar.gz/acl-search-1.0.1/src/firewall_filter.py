from pyparsing import *

class FirewallFilter(object):

    def __init__(self):
        startDelim = Literal('{').suppress()
        endDelim = Literal('}').suppress()
        word = Word(alphanums + ',:-=[]"\'_\\')
        ip_octet = Word(nums, min=1, max=3)

        ip = Combine(ip_octet + '.' + ip_octet + '.' + ip_octet + '.' + ip_octet)
        cidr = Combine(ip + Optional('/' + Word(nums, min=1, max=2) + Literal(';').suppress()))
        expr = Group(ZeroOrMore(word) + ';').suppress()
        label = word.suppress()


        source_addr_blk = Group( Keyword('source-address') + startDelim + ZeroOrMore(cidr) + endDelim)
        destination_addr_blk = Group( Keyword('destination-address').suppress() + startDelim + ZeroOrMore(cidr) + endDelim)

        from_then_blk = Group( (Keyword('from') | Keyword('then')) + startDelim + ZeroOrMore(expr) + ZeroOrMore(source_addr_blk | destination_addr_blk) + ZeroOrMore(expr) + endDelim)

        term_keyword = Keyword('term').suppress() + word

        term =  Group(term_keyword) + startDelim + ZeroOrMore(from_then_blk) + endDelim
        term_original = originalTextFor(term)
        filters = Keyword('filter').suppress() + word.suppress() + startDelim + ZeroOrMore(term) + endDelim

        doc = Keyword('firewall').suppress() + startDelim + label + ZeroOrMore(filters) + endDelim

        doc.ignore(cStyleComment)

        self.doc = doc
        self.term = term
        self.term_keyword = term_keyword
        self.term_original = term_original
        self.destination_addr_blk = destination_addr_blk


    def firewall_filter_full_grammar(self):
        return self.doc
    def firewall_filter_term(self):
        return self.term
    def firewall_filter_term_key(self):
        return self.term_keyword
    def firewall_filter_term_original(self):
        return self.term_original
    def firewall_filter_dest_addr_block(self):
        return self.destination_addr_blk
