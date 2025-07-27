// prosemirror-view@1.39.3 downloaded from https://ga.jspm.io/npm:prosemirror-view@1.39.3/dist/index.js

import {
    TextSelection as e,
    NodeSelection as t,
    Selection as n,
    AllSelection as o
} from "prosemirror-state";
import {
    DOMSerializer as i,
    Fragment as s,
    Mark as r,
    Slice as l,
    DOMParser as a
} from "prosemirror-model";
import {
    dropPoint as d
} from "prosemirror-transform";
const c = function(e) {
    for (var t = 0;; t++) {
        e = e.previousSibling;
        if (!e) return t
    }
};
const h = function(e) {
    let t = e.assignedSlot || e.parentNode;
    return t && t.nodeType == 11 ? t.host : t
};
let f = null;
const u = function(e, t, n) {
    let o = f || (f = document.createRange());
    o.setEnd(e, n == null ? e.nodeValue.length : n);
    o.setStart(e, t || 0);
    return o
};
const p = function() {
    f = null
};
const m = function(e, t, n, o) {
    return n && (y(e, t, n, o, -1) || y(e, t, n, o, 1))
};
const g = /^(img|br|input|textarea|hr)$/i;

function y(e, t, n, o, i) {
    for (;;) {
        if (e == n && t == o) return true;
        if (t == (i < 0 ? 0 : w(e))) {
            let n = e.parentNode;
            if (!n || n.nodeType != 1 || N(e) || g.test(e.nodeName) || e.contentEditable == "false") return false;
            t = c(e) + (i < 0 ? 0 : 1);
            e = n
        } else {
            if (e.nodeType != 1) return false;
            e = e.childNodes[t + (i < 0 ? -1 : 0)];
            if (e.contentEditable == "false") return false;
            t = i < 0 ? w(e) : 0
        }
    }
}

function w(e) {
    return e.nodeType == 3 ? e.nodeValue.length : e.childNodes.length
}

function b(e, t) {
    for (;;) {
        if (e.nodeType == 3 && t) return e;
        if (e.nodeType == 1 && t > 0) {
            if (e.contentEditable == "false") return null;
            e = e.childNodes[t - 1];
            t = w(e)
        } else {
            if (!e.parentNode || N(e)) return null;
            t = c(e);
            e = e.parentNode
        }
    }
}

function D(e, t) {
    for (;;) {
        if (e.nodeType == 3 && t < e.nodeValue.length) return e;
        if (e.nodeType == 1 && t < e.childNodes.length) {
            if (e.contentEditable == "false") return null;
            e = e.childNodes[t];
            t = 0
        } else {
            if (!e.parentNode || N(e)) return null;
            t = c(e) + 1;
            e = e.parentNode
        }
    }
}

function v(e, t, n) {
    for (let o = t == 0, i = t == w(e); o || i;) {
        if (e == n) return true;
        let t = c(e);
        e = e.parentNode;
        if (!e) return false;
        o = o && t == 0;
        i = i && t == w(e)
    }
}

function N(e) {
    let t;
    for (let n = e; n; n = n.parentNode)
        if (t = n.pmViewDesc) break;
    return t && t.node && t.node.isBlock && (t.dom == e || t.contentDOM == e)
}
const S = function(e) {
    return e.focusNode && m(e.focusNode, e.focusOffset, e.anchorNode, e.anchorOffset)
};

function O(e, t) {
    let n = document.createEvent("Event");
    n.initEvent("keydown", true, true);
    n.keyCode = e;
    n.key = n.code = t;
    return n
}

function C(e) {
    let t = e.activeElement;
    while (t && t.shadowRoot) t = t.shadowRoot.activeElement;
    return t
}

function M(e, t, n) {
    if (e.caretPositionFromPoint) try {
        let o = e.caretPositionFromPoint(t, n);
        if (o) return {
            node: o.offsetNode,
            offset: Math.min(w(o.offsetNode), o.offset)
        }
    } catch (e) {}
    if (e.caretRangeFromPoint) {
        let o = e.caretRangeFromPoint(t, n);
        if (o) return {
            node: o.startContainer,
            offset: Math.min(w(o.startContainer), o.startOffset)
        }
    }
}
const x = typeof navigator != "undefined" ? navigator : null;
const T = typeof document != "undefined" ? document : null;
const k = x && x.userAgent || "";
const V = /Edge\/(\d+)/.exec(k);
const E = /MSIE \d/.exec(k);
const P = /Trident\/(?:[7-9]|\d{2,})\..*rv:(\d+)/.exec(k);
const A = !!(E || P || V);
const R = E ? document.documentMode : P ? +P[1] : V ? +V[1] : 0;
const B = !A && /gecko\/(\d+)/i.test(k);
B && +(/Firefox\/(\d+)/.exec(k) || [0, 0])[1];
const I = !A && /Chrome\/(\d+)/.exec(k);
const z = !!I;
const L = I ? +I[1] : 0;
const F = !A && !!x && /Apple Computer/.test(x.vendor);
const $ = F && (/Mobile\/\w+/.test(k) || !!x && x.maxTouchPoints > 2);
const q = $ || !!x && /Mac/.test(x.platform);
const K = !!x && /Win/.test(x.platform);
const W = /Android \d/.test(k);
const H = !!T && "webkitFontSmoothing" in T.documentElement.style;
const _ = H ? +(/\bAppleWebKit\/(\d+)/.exec(navigator.userAgent) || [0, 0])[1] : 0;

function G(e) {
    let t = e.defaultView && e.defaultView.visualViewport;
    return t ? {
        left: 0,
        right: t.width,
        top: 0,
        bottom: t.height
    } : {
        left: 0,
        right: e.documentElement.clientWidth,
        top: 0,
        bottom: e.documentElement.clientHeight
    }
}

function U(e, t) {
    return typeof e == "number" ? e : e[t]
}

function j(e) {
    let t = e.getBoundingClientRect();
    let n = t.width / e.offsetWidth || 1;
    let o = t.height / e.offsetHeight || 1;
    return {
        left: t.left,
        right: t.left + e.clientWidth * n,
        top: t.top,
        bottom: t.top + e.clientHeight * o
    }
}

function X(e, t, n) {
    let o = e.someProp("scrollThreshold") || 0,
        i = e.someProp("scrollMargin") || 5;
    let s = e.dom.ownerDocument;
    for (let r = n || e.dom;;) {
        if (!r) break;
        if (r.nodeType != 1) {
            r = h(r);
            continue
        }
        let e = r;
        let n = e == s.body;
        let l = n ? G(s) : j(e);
        let a = 0,
            d = 0;
        t.top < l.top + U(o, "top") ? d = -(l.top - t.top + U(i, "top")) : t.bottom > l.bottom - U(o, "bottom") && (d = t.bottom - t.top > l.bottom - l.top ? t.top + U(i, "top") - l.top : t.bottom - l.bottom + U(i, "bottom"));
        t.left < l.left + U(o, "left") ? a = -(l.left - t.left + U(i, "left")) : t.right > l.right - U(o, "right") && (a = t.right - l.right + U(i, "right"));
        if (a || d)
            if (n) s.defaultView.scrollBy(a, d);
            else {
                let n = e.scrollLeft,
                    o = e.scrollTop;
                d && (e.scrollTop += d);
                a && (e.scrollLeft += a);
                let i = e.scrollLeft - n,
                    s = e.scrollTop - o;
                t = {
                    left: t.left - i,
                    top: t.top - s,
                    right: t.right - i,
                    bottom: t.bottom - s
                }
            } let c = n ? "fixed" : getComputedStyle(r).position;
        if (/^(fixed|sticky)$/.test(c)) break;
        r = c == "absolute" ? r.offsetParent : h(r)
    }
}

function Y(e) {
    let t = e.dom.getBoundingClientRect(),
        n = Math.max(0, t.top);
    let o, i;
    for (let s = (t.left + t.right) / 2, r = n + 1; r < Math.min(innerHeight, t.bottom); r += 5) {
        let t = e.root.elementFromPoint(s, r);
        if (!t || t == e.dom || !e.dom.contains(t)) continue;
        let l = t.getBoundingClientRect();
        if (l.top >= n - 20) {
            o = t;
            i = l.top;
            break
        }
    }
    return {
        refDOM: o,
        refTop: i,
        stack: J(e.dom)
    }
}

function J(e) {
    let t = [],
        n = e.ownerDocument;
    for (let o = e; o; o = h(o)) {
        t.push({
            dom: o,
            top: o.scrollTop,
            left: o.scrollLeft
        });
        if (e == n) break
    }
    return t
}

function Q({
    refDOM: e,
    refTop: t,
    stack: n
}) {
    let o = e ? e.getBoundingClientRect().top : 0;
    Z(n, o == 0 ? 0 : o - t)
}

function Z(e, t) {
    for (let n = 0; n < e.length; n++) {
        let {
            dom: o,
            top: i,
            left: s
        } = e[n];
        o.scrollTop != i + t && (o.scrollTop = i + t);
        o.scrollLeft != s && (o.scrollLeft = s)
    }
}
let ee = null;

function te(e) {
    if (e.setActive) return e.setActive();
    if (ee) return e.focus(ee);
    let t = J(e);
    e.focus(ee == null ? {
        get preventScroll() {
            ee = {
                preventScroll: true
            };
            return true
        }
    } : void 0);
    if (!ee) {
        ee = false;
        Z(t, 0)
    }
}

function ne(e, t) {
    let n, o, i = 2e8,
        s = 0;
    let r = t.top,
        l = t.top;
    let a, d;
    for (let c = e.firstChild, h = 0; c; c = c.nextSibling, h++) {
        let e;
        if (c.nodeType == 1) e = c.getClientRects();
        else {
            if (c.nodeType != 3) continue;
            e = u(c).getClientRects()
        }
        for (let f = 0; f < e.length; f++) {
            let u = e[f];
            if (u.top <= r && u.bottom >= l) {
                r = Math.max(u.bottom, r);
                l = Math.min(u.top, l);
                let e = u.left > t.left ? u.left - t.left : u.right < t.left ? t.left - u.right : 0;
                if (e < i) {
                    n = c;
                    i = e;
                    o = e && n.nodeType == 3 ? {
                        left: u.right < t.left ? u.right : u.left,
                        top: t.top
                    } : t;
                    c.nodeType == 1 && e && (s = h + (t.left >= (u.left + u.right) / 2 ? 1 : 0));
                    continue
                }
            } else if (u.top > t.top && !a && u.left <= t.left && u.right >= t.left) {
                a = c;
                d = {
                    left: Math.max(u.left, Math.min(u.right, t.left)),
                    top: u.top
                }
            }!n && (t.left >= u.right && t.top >= u.top || t.left >= u.left && t.top >= u.bottom) && (s = h + 1)
        }
    }
    if (!n && a) {
        n = a;
        o = d;
        i = 0
    }
    return n && n.nodeType == 3 ? oe(n, o) : !n || i && n.nodeType == 1 ? {
        node: e,
        offset: s
    } : ne(n, o)
}

function oe(e, t) {
    let n = e.nodeValue.length;
    let o = document.createRange();
    for (let i = 0; i < n; i++) {
        o.setEnd(e, i + 1);
        o.setStart(e, i);
        let n = he(o, 1);
        if (n.top != n.bottom && ie(t, n)) return {
            node: e,
            offset: i + (t.left >= (n.left + n.right) / 2 ? 1 : 0)
        }
    }
    return {
        node: e,
        offset: 0
    }
}

function ie(e, t) {
    return e.left >= t.left - 1 && e.left <= t.right + 1 && e.top >= t.top - 1 && e.top <= t.bottom + 1
}

function se(e, t) {
    let n = e.parentNode;
    return n && /^li$/i.test(n.nodeName) && t.left < e.getBoundingClientRect().left ? n : e
}

function re(e, t, n) {
    let {
        node: o,
        offset: i
    } = ne(t, n), s = -1;
    if (o.nodeType == 1 && !o.firstChild) {
        let e = o.getBoundingClientRect();
        s = e.left != e.right && n.left > (e.left + e.right) / 2 ? 1 : -1
    }
    return e.docView.posFromDOM(o, i, s)
}

function le(e, t, n, o) {
    let i = -1;
    for (let n = t, s = false;;) {
        if (n == e.dom) break;
        let t, r = e.docView.nearestDesc(n, true);
        if (!r) return null;
        if (r.dom.nodeType == 1 && (r.node.isBlock && r.parent || !r.contentDOM) && ((t = r.dom.getBoundingClientRect()).width || t.height)) {
            if (r.node.isBlock && r.parent) {
                !s && t.left > o.left || t.top > o.top ? i = r.posBefore : (!s && t.right < o.left || t.bottom < o.top) && (i = r.posAfter);
                s = true
            }
            if (!r.contentDOM && i < 0 && !r.node.isText) {
                let e = r.node.isBlock ? o.top < (t.top + t.bottom) / 2 : o.left < (t.left + t.right) / 2;
                return e ? r.posBefore : r.posAfter
            }
        }
        n = r.dom.parentNode
    }
    return i > -1 ? i : e.docView.posFromDOM(t, n, -1)
}

function ae(e, t, n) {
    let o = e.childNodes.length;
    if (o && n.top < n.bottom)
        for (let i = Math.max(0, Math.min(o - 1, Math.floor(o * (t.top - n.top) / (n.bottom - n.top)) - 2)), s = i;;) {
            let n = e.childNodes[s];
            if (n.nodeType == 1) {
                let e = n.getClientRects();
                for (let o = 0; o < e.length; o++) {
                    let i = e[o];
                    if (ie(t, i)) return ae(n, t, i)
                }
            }
            if ((s = (s + 1) % o) == i) break
        }
    return e
}

function de(e, t) {
    let n, o = e.dom.ownerDocument,
        i = 0;
    let s = M(o, t.left, t.top);
    s && ({
        node: n,
        offset: i
    } = s);
    let r = (e.root.elementFromPoint ? e.root : o).elementFromPoint(t.left, t.top);
    let l;
    if (!r || !e.dom.contains(r.nodeType != 1 ? r.parentNode : r)) {
        let n = e.dom.getBoundingClientRect();
        if (!ie(t, n)) return null;
        r = ae(e.dom, t, n);
        if (!r) return null
    }
    if (F)
        for (let e = r; n && e; e = h(e)) e.draggable && (n = void 0);
    r = se(r, t);
    if (n) {
        if (B && n.nodeType == 1) {
            i = Math.min(i, n.childNodes.length);
            if (i < n.childNodes.length) {
                let e, o = n.childNodes[i];
                o.nodeName == "IMG" && (e = o.getBoundingClientRect()).right <= t.left && e.bottom > t.top && i++
            }
        }
        let o;
        H && i && n.nodeType == 1 && (o = n.childNodes[i - 1]).nodeType == 1 && o.contentEditable == "false" && o.getBoundingClientRect().top >= t.top && i--;
        n == e.dom && i == n.childNodes.length - 1 && n.lastChild.nodeType == 1 && t.top > n.lastChild.getBoundingClientRect().bottom ? l = e.state.doc.content.size : i != 0 && n.nodeType == 1 && n.childNodes[i - 1].nodeName == "BR" || (l = le(e, n, i, t))
    }
    l == null && (l = re(e, r, t));
    let a = e.docView.nearestDesc(r, true);
    return {
        pos: l,
        inside: a ? a.posAtStart - a.border : -1
    }
}

function ce(e) {
    return e.top < e.bottom || e.left < e.right
}

function he(e, t) {
    let n = e.getClientRects();
    if (n.length) {
        let e = n[t < 0 ? 0 : n.length - 1];
        if (ce(e)) return e
    }
    return Array.prototype.find.call(n, ce) || e.getBoundingClientRect()
}
const fe = /[\u0590-\u05f4\u0600-\u06ff\u0700-\u08ac]/;

function ue(e, t, n) {
    let {
        node: o,
        offset: i,
        atom: s
    } = e.docView.domFromPos(t, n < 0 ? -1 : 1);
    let r = H || B;
    if (o.nodeType == 3) {
        if (!r || !fe.test(o.nodeValue) && (n < 0 ? i : i != o.nodeValue.length)) {
            let e = i,
                t = i,
                s = n < 0 ? 1 : -1;
            if (n < 0 && !i) {
                t++;
                s = -1
            } else if (n >= 0 && i == o.nodeValue.length) {
                e--;
                s = 1
            } else n < 0 ? e-- : t++;
            return pe(he(u(o, e, t), s), s < 0)
        } {
            let e = he(u(o, i, i), n);
            if (B && i && /\s/.test(o.nodeValue[i - 1]) && i < o.nodeValue.length) {
                let t = he(u(o, i - 1, i - 1), -1);
                if (t.top == e.top) {
                    let n = he(u(o, i, i + 1), -1);
                    if (n.top != e.top) return pe(n, n.left < t.left)
                }
            }
            return e
        }
    }
    let l = e.state.doc.resolve(t - (s || 0));
    if (!l.parent.inlineContent) {
        if (s == null && i && (n < 0 || i == w(o))) {
            let e = o.childNodes[i - 1];
            if (e.nodeType == 1) return me(e.getBoundingClientRect(), false)
        }
        if (s == null && i < w(o)) {
            let e = o.childNodes[i];
            if (e.nodeType == 1) return me(e.getBoundingClientRect(), true)
        }
        return me(o.getBoundingClientRect(), n >= 0)
    }
    if (s == null && i && (n < 0 || i == w(o))) {
        let e = o.childNodes[i - 1];
        let t = e.nodeType == 3 ? u(e, w(e) - (r ? 0 : 1)) : e.nodeType != 1 || e.nodeName == "BR" && e.nextSibling ? null : e;
        if (t) return pe(he(t, 1), false)
    }
    if (s == null && i < w(o)) {
        let e = o.childNodes[i];
        while (e.pmViewDesc && e.pmViewDesc.ignoreForCoords) e = e.nextSibling;
        let t = e ? e.nodeType == 3 ? u(e, 0, r ? 0 : 1) : e.nodeType == 1 ? e : null : null;
        if (t) return pe(he(t, -1), true)
    }
    return pe(he(o.nodeType == 3 ? u(o) : o, -n), n >= 0)
}

function pe(e, t) {
    if (e.width == 0) return e;
    let n = t ? e.left : e.right;
    return {
        top: e.top,
        bottom: e.bottom,
        left: n,
        right: n
    }
}

function me(e, t) {
    if (e.height == 0) return e;
    let n = t ? e.top : e.bottom;
    return {
        top: n,
        bottom: n,
        left: e.left,
        right: e.right
    }
}

function ge(e, t, n) {
    let o = e.state,
        i = e.root.activeElement;
    o != t && e.updateState(t);
    i != e.dom && e.focus();
    try {
        return n()
    } finally {
        o != t && e.updateState(o);
        i != e.dom && i && i.focus()
    }
}

function ye(e, t, n) {
    let o = t.selection;
    let i = n == "up" ? o.$from : o.$to;
    return ge(e, t, (() => {
        let {
            node: t
        } = e.docView.domFromPos(i.pos, n == "up" ? -1 : 1);
        for (;;) {
            let n = e.docView.nearestDesc(t, true);
            if (!n) break;
            if (n.node.isBlock) {
                t = n.contentDOM || n.dom;
                break
            }
            t = n.dom.parentNode
        }
        let o = ue(e, i.pos, 1);
        for (let e = t.firstChild; e; e = e.nextSibling) {
            let t;
            if (e.nodeType == 1) t = e.getClientRects();
            else {
                if (e.nodeType != 3) continue;
                t = u(e, 0, e.nodeValue.length).getClientRects()
            }
            for (let e = 0; e < t.length; e++) {
                let i = t[e];
                if (i.bottom > i.top + 1 && (n == "up" ? o.top - i.top > 2 * (i.bottom - o.top) : i.bottom - o.bottom > 2 * (o.bottom - i.top))) return false
            }
        }
        return true
    }))
}
const we = /[\u0590-\u08ac]/;

function be(e, t, n) {
    let {
        $head: o
    } = t.selection;
    if (!o.parent.isTextblock) return false;
    let i = o.parentOffset,
        s = !i,
        r = i == o.parent.content.size;
    let l = e.domSelection();
    return l ? we.test(o.parent.textContent) && l.modify ? ge(e, t, (() => {
        let {
            focusNode: t,
            focusOffset: i,
            anchorNode: s,
            anchorOffset: r
        } = e.domSelectionRange();
        let a = l.caretBidiLevel;
        l.modify("move", n, "character");
        let d = o.depth ? e.docView.domAfterPos(o.before()) : e.dom;
        let {
            focusNode: c,
            focusOffset: h
        } = e.domSelectionRange();
        let f = c && !d.contains(c.nodeType == 1 ? c : c.parentNode) || t == c && i == h;
        try {
            l.collapse(s, r);
            t && (t != s || i != r) && l.extend && l.extend(t, i)
        } catch (e) {}
        a != null && (l.caretBidiLevel = a);
        return f
    })) : n == "left" || n == "backward" ? s : r : o.pos == o.start() || o.pos == o.end()
}
let De = null;
let ve = null;
let Ne = false;

function Se(e, t, n) {
    if (De == t && ve == n) return Ne;
    De = t;
    ve = n;
    return Ne = n == "up" || n == "down" ? ye(e, t, n) : be(e, t, n)
}
const Oe = 0,
    Ce = 1,
    Me = 2,
    xe = 3;
class ViewDesc {
    constructor(e, t, n, o) {
        this.parent = e;
        this.children = t;
        this.dom = n;
        this.contentDOM = o;
        this.dirty = Oe;
        n.pmViewDesc = this
    }
    matchesWidget(e) {
        return false
    }
    matchesMark(e) {
        return false
    }
    matchesNode(e, t, n) {
        return false
    }
    matchesHack(e) {
        return false
    }
    parseRule() {
        return null
    }
    stopEvent(e) {
        return false
    }
    get size() {
        let e = 0;
        for (let t = 0; t < this.children.length; t++) e += this.children[t].size;
        return e
    }
    get border() {
        return 0
    }
    destroy() {
        this.parent = void 0;
        this.dom.pmViewDesc == this && (this.dom.pmViewDesc = void 0);
        for (let e = 0; e < this.children.length; e++) this.children[e].destroy()
    }
    posBeforeChild(e) {
        for (let t = 0, n = this.posAtStart;; t++) {
            let o = this.children[t];
            if (o == e) return n;
            n += o.size
        }
    }
    get posBefore() {
        return this.parent.posBeforeChild(this)
    }
    get posAtStart() {
        return this.parent ? this.parent.posBeforeChild(this) + this.border : 0
    }
    get posAfter() {
        return this.posBefore + this.size
    }
    get posAtEnd() {
        return this.posAtStart + this.size - 2 * this.border
    }
    localPosFromDOM(e, t, n) {
        if (this.contentDOM && this.contentDOM.contains(e.nodeType == 1 ? e : e.parentNode)) {
            if (n < 0) {
                let n, o;
                if (e == this.contentDOM) n = e.childNodes[t - 1];
                else {
                    while (e.parentNode != this.contentDOM) e = e.parentNode;
                    n = e.previousSibling
                }
                while (n && !((o = n.pmViewDesc) && o.parent == this)) n = n.previousSibling;
                return n ? this.posBeforeChild(o) + o.size : this.posAtStart
            } {
                let n, o;
                if (e == this.contentDOM) n = e.childNodes[t];
                else {
                    while (e.parentNode != this.contentDOM) e = e.parentNode;
                    n = e.nextSibling
                }
                while (n && !((o = n.pmViewDesc) && o.parent == this)) n = n.nextSibling;
                return n ? this.posBeforeChild(o) : this.posAtEnd
            }
        }
        let o;
        if (e == this.dom && this.contentDOM) o = t > c(this.contentDOM);
        else if (this.contentDOM && this.contentDOM != this.dom && this.dom.contains(this.contentDOM)) o = e.compareDocumentPosition(this.contentDOM) & 2;
        else if (this.dom.firstChild) {
            if (t == 0)
                for (let t = e;; t = t.parentNode) {
                    if (t == this.dom) {
                        o = false;
                        break
                    }
                    if (t.previousSibling) break
                }
            if (o == null && t == e.childNodes.length)
                for (let t = e;; t = t.parentNode) {
                    if (t == this.dom) {
                        o = true;
                        break
                    }
                    if (t.nextSibling) break
                }
        }
        return (o == null ? n > 0 : o) ? this.posAtEnd : this.posAtStart
    }
    nearestDesc(e, t = false) {
        for (let n = true, o = e; o; o = o.parentNode) {
            let i, s = this.getDesc(o);
            if (s && (!t || s.node)) {
                if (!n || !(i = s.nodeDOM) || (i.nodeType == 1 ? i.contains(e.nodeType == 1 ? e : e.parentNode) : i == e)) return s;
                n = false
            }
        }
    }
    getDesc(e) {
        let t = e.pmViewDesc;
        for (let e = t; e; e = e.parent)
            if (e == this) return t
    }
    posFromDOM(e, t, n) {
        for (let o = e; o; o = o.parentNode) {
            let i = this.getDesc(o);
            if (i) return i.localPosFromDOM(e, t, n)
        }
        return -1
    }
    descAt(e) {
        for (let t = 0, n = 0; t < this.children.length; t++) {
            let o = this.children[t],
                i = n + o.size;
            if (n == e && i != n) {
                while (!o.border && o.children.length)
                    for (let e = 0; e < o.children.length; e++) {
                        let t = o.children[e];
                        if (t.size) {
                            o = t;
                            break
                        }
                    }
                return o
            }
            if (e < i) return o.descAt(e - n - o.border);
            n = i
        }
    }
    domFromPos(e, t) {
        if (!this.contentDOM) return {
            node: this.dom,
            offset: 0,
            atom: e + 1
        };
        let n = 0,
            o = 0;
        for (let t = 0; n < this.children.length; n++) {
            let i = this.children[n],
                s = t + i.size;
            if (s > e || i instanceof TrailingHackViewDesc) {
                o = e - t;
                break
            }
            t = s
        }
        if (o) return this.children[n].domFromPos(o - this.children[n].border, t);
        for (let e; n && !(e = this.children[n - 1]).size && e instanceof WidgetViewDesc && e.side >= 0; n--);
        if (t <= 0) {
            let e, o = true;
            for (;; n--, o = false) {
                e = n ? this.children[n - 1] : null;
                if (!e || e.dom.parentNode == this.contentDOM) break
            }
            return e && t && o && !e.border && !e.domAtom ? e.domFromPos(e.size, t) : {
                node: this.contentDOM,
                offset: e ? c(e.dom) + 1 : 0
            }
        } {
            let e, o = true;
            for (;; n++, o = false) {
                e = n < this.children.length ? this.children[n] : null;
                if (!e || e.dom.parentNode == this.contentDOM) break
            }
            return e && o && !e.border && !e.domAtom ? e.domFromPos(0, t) : {
                node: this.contentDOM,
                offset: e ? c(e.dom) : this.contentDOM.childNodes.length
            }
        }
    }
    parseRange(e, t, n = 0) {
        if (this.children.length == 0) return {
            node: this.contentDOM,
            from: e,
            to: t,
            fromOffset: 0,
            toOffset: this.contentDOM.childNodes.length
        };
        let o = -1,
            i = -1;
        for (let s = n, r = 0;; r++) {
            let n = this.children[r],
                l = s + n.size;
            if (o == -1 && e <= l) {
                let i = s + n.border;
                if (e >= i && t <= l - n.border && n.node && n.contentDOM && this.contentDOM.contains(n.contentDOM)) return n.parseRange(e, t, i);
                e = s;
                for (let t = r; t > 0; t--) {
                    let n = this.children[t - 1];
                    if (n.size && n.dom.parentNode == this.contentDOM && !n.emptyChildAt(1)) {
                        o = c(n.dom) + 1;
                        break
                    }
                    e -= n.size
                }
                o == -1 && (o = 0)
            }
            if (o > -1 && (l > t || r == this.children.length - 1)) {
                t = l;
                for (let e = r + 1; e < this.children.length; e++) {
                    let n = this.children[e];
                    if (n.size && n.dom.parentNode == this.contentDOM && !n.emptyChildAt(-1)) {
                        i = c(n.dom);
                        break
                    }
                    t += n.size
                }
                i == -1 && (i = this.contentDOM.childNodes.length);
                break
            }
            s = l
        }
        return {
            node: this.contentDOM,
            from: e,
            to: t,
            fromOffset: o,
            toOffset: i
        }
    }
    emptyChildAt(e) {
        if (this.border || !this.contentDOM || !this.children.length) return false;
        let t = this.children[e < 0 ? 0 : this.children.length - 1];
        return t.size == 0 || t.emptyChildAt(e)
    }
    domAfterPos(e) {
        let {
            node: t,
            offset: n
        } = this.domFromPos(e, 0);
        if (t.nodeType != 1 || n == t.childNodes.length) throw new RangeError("No node after pos " + e);
        return t.childNodes[n]
    }
    setSelection(e, t, n, o = false) {
        let i = Math.min(e, t),
            s = Math.max(e, t);
        for (let r = 0, l = 0; r < this.children.length; r++) {
            let a = this.children[r],
                d = l + a.size;
            if (i > l && s < d) return a.setSelection(e - l - a.border, t - l - a.border, n, o);
            l = d
        }
        let r = this.domFromPos(e, e ? -1 : 1);
        let l = t == e ? r : this.domFromPos(t, t ? -1 : 1);
        let a = n.root.getSelection();
        let d = n.domSelectionRange();
        let h = false;
        if ((B || F) && e == t) {
            let {
                node: e,
                offset: t
            } = r;
            if (e.nodeType == 3) {
                h = !!(t && e.nodeValue[t - 1] == "\n");
                if (h && t == e.nodeValue.length)
                    for (let t, n = e; n; n = n.parentNode) {
                        if (t = n.nextSibling) {
                            t.nodeName == "BR" && (r = l = {
                                node: t.parentNode,
                                offset: c(t) + 1
                            });
                            break
                        }
                        let e = n.pmViewDesc;
                        if (e && e.node && e.node.isBlock) break
                    }
            } else {
                let n = e.childNodes[t - 1];
                h = n && (n.nodeName == "BR" || n.contentEditable == "false")
            }
        }
        if (B && d.focusNode && d.focusNode != l.node && d.focusNode.nodeType == 1) {
            let e = d.focusNode.childNodes[d.focusOffset];
            e && e.contentEditable == "false" && (o = true)
        }
        if (!(o || h && F) && m(r.node, r.offset, d.anchorNode, d.anchorOffset) && m(l.node, l.offset, d.focusNode, d.focusOffset)) return;
        let f = false;
        if ((a.extend || e == t) && !h) {
            a.collapse(r.node, r.offset);
            try {
                e != t && a.extend(l.node, l.offset);
                f = true
            } catch (e) {}
        }
        if (!f) {
            if (e > t) {
                let e = r;
                r = l;
                l = e
            }
            let n = document.createRange();
            n.setEnd(l.node, l.offset);
            n.setStart(r.node, r.offset);
            a.removeAllRanges();
            a.addRange(n)
        }
    }
    ignoreMutation(e) {
        return !this.contentDOM && e.type != "selection"
    }
    get contentLost() {
        return this.contentDOM && this.contentDOM != this.dom && !this.dom.contains(this.contentDOM)
    }
    markDirty(e, t) {
        for (let n = 0, o = 0; o < this.children.length; o++) {
            let i = this.children[o],
                s = n + i.size;
            if (n == s ? e <= s && t >= n : e < s && t > n) {
                let o = n + i.border,
                    r = s - i.border;
                if (e >= o && t <= r) {
                    this.dirty = e == n || t == s ? Me : Ce;
                    e != o || t != r || !i.contentLost && i.dom.parentNode == this.contentDOM ? i.markDirty(e - o, t - o) : i.dirty = xe;
                    return
                }
                i.dirty = i.dom != i.contentDOM || i.dom.parentNode != this.contentDOM || i.children.length ? xe : Me
            }
            n = s
        }
        this.dirty = Me
    }
    markParentsDirty() {
        let e = 1;
        for (let t = this.parent; t; t = t.parent, e++) {
            let n = e == 1 ? Me : Ce;
            t.dirty < n && (t.dirty = n)
        }
    }
    get domAtom() {
        return false
    }
    get ignoreForCoords() {
        return false
    }
    isText(e) {
        return false
    }
}
class WidgetViewDesc extends ViewDesc {
    constructor(e, t, n, o) {
        let i, s = t.type.toDOM;
        typeof s == "function" && (s = s(n, (() => i ? i.parent ? i.parent.posBeforeChild(i) : void 0 : o)));
        if (!t.type.spec.raw) {
            if (s.nodeType != 1) {
                let e = document.createElement("span");
                e.appendChild(s);
                s = e
            }
            s.contentEditable = "false";
            s.classList.add("ProseMirror-widget")
        }
        super(e, [], s, null);
        this.widget = t;
        this.widget = t;
        i = this
    }
    matchesWidget(e) {
        return this.dirty == Oe && e.type.eq(this.widget.type)
    }
    parseRule() {
        return {
            ignore: true
        }
    }
    stopEvent(e) {
        let t = this.widget.spec.stopEvent;
        return !!t && t(e)
    }
    ignoreMutation(e) {
        return e.type != "selection" || this.widget.spec.ignoreSelection
    }
    destroy() {
        this.widget.type.destroy(this.dom);
        super.destroy()
    }
    get domAtom() {
        return true
    }
    get side() {
        return this.widget.type.side
    }
}
class CompositionViewDesc extends ViewDesc {
    constructor(e, t, n, o) {
        super(e, [], t, null);
        this.textDOM = n;
        this.text = o
    }
    get size() {
        return this.text.length
    }
    localPosFromDOM(e, t) {
        return e != this.textDOM ? this.posAtStart + (t ? this.size : 0) : this.posAtStart + t
    }
    domFromPos(e) {
        return {
            node: this.textDOM,
            offset: e
        }
    }
    ignoreMutation(e) {
        return e.type === "characterData" && e.target.nodeValue == e.oldValue
    }
}
class MarkViewDesc extends ViewDesc {
    constructor(e, t, n, o, i) {
        super(e, [], n, o);
        this.mark = t;
        this.spec = i
    }
    static create(e, t, n, o) {
        let s = o.nodeViews[t.type.name];
        let r = s && s(t, o, n);
        r && r.dom || (r = i.renderSpec(document, t.type.spec.toDOM(t, n), null, t.attrs));
        return new MarkViewDesc(e, t, r.dom, r.contentDOM || r.dom, r)
    }
    parseRule() {
        return this.dirty & xe || this.mark.type.spec.reparseInView ? null : {
            mark: this.mark.type.name,
            attrs: this.mark.attrs,
            contentElement: this.contentDOM
        }
    }
    matchesMark(e) {
        return this.dirty != xe && this.mark.eq(e)
    }
    markDirty(e, t) {
        super.markDirty(e, t);
        if (this.dirty != Oe) {
            let e = this.parent;
            while (!e.node) e = e.parent;
            e.dirty < this.dirty && (e.dirty = this.dirty);
            this.dirty = Oe
        }
    }
    slice(e, t, n) {
        let o = MarkViewDesc.create(this.parent, this.mark, true, n);
        let i = this.children,
            s = this.size;
        t < s && (i = We(i, t, s, n));
        e > 0 && (i = We(i, 0, e, n));
        for (let e = 0; e < i.length; e++) i[e].parent = o;
        o.children = i;
        return o
    }
    ignoreMutation(e) {
        return this.spec.ignoreMutation ? this.spec.ignoreMutation(e) : super.ignoreMutation(e)
    }
    destroy() {
        this.spec.destroy && this.spec.destroy();
        super.destroy()
    }
}
class NodeViewDesc extends ViewDesc {
    constructor(e, t, n, o, i, s, r, l, a) {
        super(e, [], i, s);
        this.node = t;
        this.outerDeco = n;
        this.innerDeco = o;
        this.nodeDOM = r
    }
    static create(e, t, n, o, s, r) {
        let l, a = s.nodeViews[t.type.name];
        let d = a && a(t, s, (() => l ? l.parent ? l.parent.posBeforeChild(l) : void 0 : r), n, o);
        let c = d && d.dom,
            h = d && d.contentDOM;
        if (t.isText)
            if (c) {
                if (c.nodeType != 3) throw new RangeError("Text must be rendered as a DOM text node")
            } else c = document.createTextNode(t.text);
        else if (!c) {
            let e = i.renderSpec(document, t.type.spec.toDOM(t), null, t.attrs);
            ({
                dom: c,
                contentDOM: h
            } = e)
        }
        if (!h && !t.isText && c.nodeName != "BR") {
            c.hasAttribute("contenteditable") || (c.contentEditable = "false");
            t.type.spec.draggable && (c.draggable = true)
        }
        let f = c;
        c = Be(c, n, t);
        return d ? l = new CustomNodeViewDesc(e, t, n, o, c, h || null, f, d, s, r + 1) : t.isText ? new TextViewDesc(e, t, n, o, c, f, s) : new NodeViewDesc(e, t, n, o, c, h || null, f, s, r + 1)
    }
    parseRule() {
        if (this.node.type.spec.reparseInView) return null;
        let e = {
            node: this.node.type.name,
            attrs: this.node.attrs
        };
        this.node.type.whitespace == "pre" && (e.preserveWhitespace = "full");
        if (this.contentDOM)
            if (this.contentLost) {
                for (let t = this.children.length - 1; t >= 0; t--) {
                    let n = this.children[t];
                    if (this.dom.contains(n.dom.parentNode)) {
                        e.contentElement = n.dom.parentNode;
                        break
                    }
                }
                e.contentElement || (e.getContent = () => s.empty)
            } else e.contentElement = this.contentDOM;
        else e.getContent = () => this.node.content;
        return e
    }
    matchesNode(e, t, n) {
        return this.dirty == Oe && e.eq(this.node) && Ie(t, this.outerDeco) && n.eq(this.innerDeco)
    }
    get size() {
        return this.node.nodeSize
    }
    get border() {
        return this.node.isLeaf ? 0 : 1
    }
    updateChildren(e, t) {
        let n = this.node.inlineContent,
            o = t;
        let i = e.composing ? this.localCompositionInfo(e, t) : null;
        let s = i && i.pos > -1 ? i : null;
        let l = i && i.pos < 0;
        let a = new ViewTreeUpdater(this, s && s.node, e);
        $e(this.node, this.innerDeco, ((t, i, s) => {
            t.spec.marks ? a.syncToMarks(t.spec.marks, n, e) : t.type.side >= 0 && !s && a.syncToMarks(i == this.node.childCount ? r.none : this.node.child(i).marks, n, e);
            a.placeWidget(t, e, o)
        }), ((t, s, r, d) => {
            a.syncToMarks(t.marks, n, e);
            let c;
            a.findNodeMatch(t, s, r, d) || l && e.state.selection.from > o && e.state.selection.to < o + t.nodeSize && (c = a.findIndexWithChild(i.node)) > -1 && a.updateNodeAt(t, s, r, c, e) || a.updateNextNode(t, s, r, e, d, o) || a.addNode(t, s, r, e, o);
            o += t.nodeSize
        }));
        a.syncToMarks([], n, e);
        this.node.isTextblock && a.addTextblockHacks();
        a.destroyRest();
        if (a.changed || this.dirty == Me) {
            s && this.protectLocalComposition(e, s);
            ke(this.contentDOM, this.children, e);
            $ && qe(this.dom)
        }
    }
    localCompositionInfo(t, n) {
        let {
            from: o,
            to: i
        } = t.state.selection;
        if (!(t.state.selection instanceof e) || o < n || i > n + this.node.content.size) return null;
        let s = t.input.compositionNode;
        if (!s || !this.dom.contains(s.parentNode)) return null;
        if (this.node.inlineContent) {
            let e = s.nodeValue;
            let t = Ke(this.node.content, e, o - n, i - n);
            return t < 0 ? null : {
                node: s,
                pos: t,
                text: e
            }
        }
        return {
            node: s,
            pos: -1,
            text: ""
        }
    }
    protectLocalComposition(e, {
        node: t,
        pos: n,
        text: o
    }) {
        if (this.getDesc(t)) return;
        let i = t;
        for (;; i = i.parentNode) {
            if (i.parentNode == this.contentDOM) break;
            while (i.previousSibling) i.parentNode.removeChild(i.previousSibling);
            while (i.nextSibling) i.parentNode.removeChild(i.nextSibling);
            i.pmViewDesc && (i.pmViewDesc = void 0)
        }
        let s = new CompositionViewDesc(this, i, t, o);
        e.input.compositionNodes.push(s);
        this.children = We(this.children, n, n + o.length, e, s)
    }
    update(e, t, n, o) {
        if (this.dirty == xe || !e.sameMarkup(this.node)) return false;
        this.updateInner(e, t, n, o);
        return true
    }
    updateInner(e, t, n, o) {
        this.updateOuterDeco(t);
        this.node = e;
        this.innerDeco = n;
        this.contentDOM && this.updateChildren(o, this.posAtStart);
        this.dirty = Oe
    }
    updateOuterDeco(e) {
        if (Ie(e, this.outerDeco)) return;
        let t = this.nodeDOM.nodeType != 1;
        let n = this.dom;
        this.dom = Ae(this.dom, this.nodeDOM, Pe(this.outerDeco, this.node, t), Pe(e, this.node, t));
        if (this.dom != n) {
            n.pmViewDesc = void 0;
            this.dom.pmViewDesc = this
        }
        this.outerDeco = e
    }
    selectNode() {
        this.nodeDOM.nodeType == 1 && this.nodeDOM.classList.add("ProseMirror-selectednode");
        !this.contentDOM && this.node.type.spec.draggable || (this.dom.draggable = true)
    }
    deselectNode() {
        if (this.nodeDOM.nodeType == 1) {
            this.nodeDOM.classList.remove("ProseMirror-selectednode");
            !this.contentDOM && this.node.type.spec.draggable || this.dom.removeAttribute("draggable")
        }
    }
    get domAtom() {
        return this.node.isAtom
    }
}

function Te(e, t, n, o, i) {
    Be(o, t, e);
    let s = new NodeViewDesc(void 0, e, t, n, o, o, o, i, 0);
    s.contentDOM && s.updateChildren(i, 0);
    return s
}
class TextViewDesc extends NodeViewDesc {
    constructor(e, t, n, o, i, s, r) {
        super(e, t, n, o, i, null, s, r, 0)
    }
    parseRule() {
        let e = this.nodeDOM.parentNode;
        while (e && e != this.dom && !e.pmIsDeco) e = e.parentNode;
        return {
            skip: e || true
        }
    }
    update(e, t, n, o) {
        if (this.dirty == xe || this.dirty != Oe && !this.inParent() || !e.sameMarkup(this.node)) return false;
        this.updateOuterDeco(t);
        if ((this.dirty != Oe || e.text != this.node.text) && e.text != this.nodeDOM.nodeValue) {
            this.nodeDOM.nodeValue = e.text;
            o.trackWrites == this.nodeDOM && (o.trackWrites = null)
        }
        this.node = e;
        this.dirty = Oe;
        return true
    }
    inParent() {
        let e = this.parent.contentDOM;
        for (let t = this.nodeDOM; t; t = t.parentNode)
            if (t == e) return true;
        return false
    }
    domFromPos(e) {
        return {
            node: this.nodeDOM,
            offset: e
        }
    }
    localPosFromDOM(e, t, n) {
        return e == this.nodeDOM ? this.posAtStart + Math.min(t, this.node.text.length) : super.localPosFromDOM(e, t, n)
    }
    ignoreMutation(e) {
        return e.type != "characterData" && e.type != "selection"
    }
    slice(e, t, n) {
        let o = this.node.cut(e, t),
            i = document.createTextNode(o.text);
        return new TextViewDesc(this.parent, o, this.outerDeco, this.innerDeco, i, i, n)
    }
    markDirty(e, t) {
        super.markDirty(e, t);
        this.dom == this.nodeDOM || e != 0 && t != this.nodeDOM.nodeValue.length || (this.dirty = xe)
    }
    get domAtom() {
        return false
    }
    isText(e) {
        return this.node.text == e
    }
}
class TrailingHackViewDesc extends ViewDesc {
    parseRule() {
        return {
            ignore: true
        }
    }
    matchesHack(e) {
        return this.dirty == Oe && this.dom.nodeName == e
    }
    get domAtom() {
        return true
    }
    get ignoreForCoords() {
        return this.dom.nodeName == "IMG"
    }
}
class CustomNodeViewDesc extends NodeViewDesc {
    constructor(e, t, n, o, i, s, r, l, a, d) {
        super(e, t, n, o, i, s, r, a, d);
        this.spec = l
    }
    update(e, t, n, o) {
        if (this.dirty == xe) return false;
        if (this.spec.update && (this.node.type == e.type || this.spec.multiType)) {
            let i = this.spec.update(e, t, n);
            i && this.updateInner(e, t, n, o);
            return i
        }
        return !(!this.contentDOM && !e.isLeaf) && super.update(e, t, n, o)
    }
    selectNode() {
        this.spec.selectNode ? this.spec.selectNode() : super.selectNode()
    }
    deselectNode() {
        this.spec.deselectNode ? this.spec.deselectNode() : super.deselectNode()
    }
    setSelection(e, t, n, o) {
        this.spec.setSelection ? this.spec.setSelection(e, t, n.root) : super.setSelection(e, t, n, o)
    }
    destroy() {
        this.spec.destroy && this.spec.destroy();
        super.destroy()
    }
    stopEvent(e) {
        return !!this.spec.stopEvent && this.spec.stopEvent(e)
    }
    ignoreMutation(e) {
        return this.spec.ignoreMutation ? this.spec.ignoreMutation(e) : super.ignoreMutation(e)
    }
}

function ke(e, t, n) {
    let o = e.firstChild,
        i = false;
    for (let s = 0; s < t.length; s++) {
        let r = t[s],
            l = r.dom;
        if (l.parentNode == e) {
            while (l != o) {
                o = ze(o);
                i = true
            }
            o = o.nextSibling
        } else {
            i = true;
            e.insertBefore(l, o)
        }
        if (r instanceof MarkViewDesc) {
            let t = o ? o.previousSibling : e.lastChild;
            ke(r.contentDOM, r.children, n);
            o = t ? t.nextSibling : e.firstChild
        }
    }
    while (o) {
        o = ze(o);
        i = true
    }
    i && n.trackWrites == e && (n.trackWrites = null)
}
const Ve = function(e) {
    e && (this.nodeName = e)
};
Ve.prototype = Object.create(null);
const Ee = [new Ve];

function Pe(e, t, n) {
    if (e.length == 0) return Ee;
    let o = n ? Ee[0] : new Ve,
        i = [o];
    for (let s = 0; s < e.length; s++) {
        let r = e[s].type.attrs;
        if (r) {
            r.nodeName && i.push(o = new Ve(r.nodeName));
            for (let e in r) {
                let s = r[e];
                if (s != null) {
                    n && i.length == 1 && i.push(o = new Ve(t.isInline ? "span" : "div"));
                    e == "class" ? o.class = (o.class ? o.class + " " : "") + s : e == "style" ? o.style = (o.style ? o.style + ";" : "") + s : e != "nodeName" && (o[e] = s)
                }
            }
        }
    }
    return i
}

function Ae(e, t, n, o) {
    if (n == Ee && o == Ee) return t;
    let i = t;
    for (let t = 0; t < o.length; t++) {
        let s = o[t],
            r = n[t];
        if (t) {
            let t;
            if (r && r.nodeName == s.nodeName && i != e && (t = i.parentNode) && t.nodeName.toLowerCase() == s.nodeName) i = t;
            else {
                t = document.createElement(s.nodeName);
                t.pmIsDeco = true;
                t.appendChild(i);
                r = Ee[0];
                i = t
            }
        }
        Re(i, r || Ee[0], s)
    }
    return i
}

function Re(e, t, n) {
    for (let o in t) o == "class" || o == "style" || o == "nodeName" || o in n || e.removeAttribute(o);
    for (let o in n) o != "class" && o != "style" && o != "nodeName" && n[o] != t[o] && e.setAttribute(o, n[o]);
    if (t.class != n.class) {
        let o = t.class ? t.class.split(" ").filter(Boolean) : [];
        let i = n.class ? n.class.split(" ").filter(Boolean) : [];
        for (let t = 0; t < o.length; t++) i.indexOf(o[t]) == -1 && e.classList.remove(o[t]);
        for (let t = 0; t < i.length; t++) o.indexOf(i[t]) == -1 && e.classList.add(i[t]);
        e.classList.length == 0 && e.removeAttribute("class")
    }
    if (t.style != n.style) {
        if (t.style) {
            let n, o = /\s*([\w\-\xa1-\uffff]+)\s*:(?:"(?:\\.|[^"])*"|'(?:\\.|[^'])*'|\(.*?\)|[^;])*/g;
            while (n = o.exec(t.style)) e.style.removeProperty(n[1])
        }
        n.style && (e.style.cssText += n.style)
    }
}

function Be(e, t, n) {
    return Ae(e, e, Ee, Pe(t, n, e.nodeType != 1))
}

function Ie(e, t) {
    if (e.length != t.length) return false;
    for (let n = 0; n < e.length; n++)
        if (!e[n].type.eq(t[n].type)) return false;
    return true
}

function ze(e) {
    let t = e.nextSibling;
    e.parentNode.removeChild(e);
    return t
}
class ViewTreeUpdater {
    constructor(e, t, n) {
        this.lock = t;
        this.view = n;
        this.index = 0;
        this.stack = [];
        this.changed = false;
        this.top = e;
        this.preMatch = Le(e.node.content, e)
    }
    destroyBetween(e, t) {
        if (e != t) {
            for (let n = e; n < t; n++) this.top.children[n].destroy();
            this.top.children.splice(e, t - e);
            this.changed = true
        }
    }
    destroyRest() {
        this.destroyBetween(this.index, this.top.children.length)
    }
    syncToMarks(e, t, n) {
        let o = 0,
            i = this.stack.length >> 1;
        let s = Math.min(i, e.length);
        while (o < s && (o == i - 1 ? this.top : this.stack[o + 1 << 1]).matchesMark(e[o]) && e[o].type.spec.spanning !== false) o++;
        while (o < i) {
            this.destroyRest();
            this.top.dirty = Oe;
            this.index = this.stack.pop();
            this.top = this.stack.pop();
            i--
        }
        while (i < e.length) {
            this.stack.push(this.top, this.index + 1);
            let o = -1;
            for (let t = this.index; t < Math.min(this.index + 3, this.top.children.length); t++) {
                let n = this.top.children[t];
                if (n.matchesMark(e[i]) && !this.isLocked(n.dom)) {
                    o = t;
                    break
                }
            }
            if (o > -1) {
                if (o > this.index) {
                    this.changed = true;
                    this.destroyBetween(this.index, o)
                }
                this.top = this.top.children[this.index]
            } else {
                let o = MarkViewDesc.create(this.top, e[i], t, n);
                this.top.children.splice(this.index, 0, o);
                this.top = o;
                this.changed = true
            }
            this.index = 0;
            i++
        }
    }
    findNodeMatch(e, t, n, o) {
        let i, s = -1;
        if (o >= this.preMatch.index && (i = this.preMatch.matches[o - this.preMatch.index]).parent == this.top && i.matchesNode(e, t, n)) s = this.top.children.indexOf(i, this.index);
        else
            for (let o = this.index, i = Math.min(this.top.children.length, o + 5); o < i; o++) {
                let i = this.top.children[o];
                if (i.matchesNode(e, t, n) && !this.preMatch.matched.has(i)) {
                    s = o;
                    break
                }
            }
        if (s < 0) return false;
        this.destroyBetween(this.index, s);
        this.index++;
        return true
    }
    updateNodeAt(e, t, n, o, i) {
        let s = this.top.children[o];
        s.dirty == xe && s.dom == s.contentDOM && (s.dirty = Me);
        if (!s.update(e, t, n, i)) return false;
        this.destroyBetween(this.index, o);
        this.index++;
        return true
    }
    findIndexWithChild(e) {
        for (;;) {
            let t = e.parentNode;
            if (!t) return -1;
            if (t == this.top.contentDOM) {
                let t = e.pmViewDesc;
                if (t)
                    for (let e = this.index; e < this.top.children.length; e++)
                        if (this.top.children[e] == t) return e;
                return -1
            }
            e = t
        }
    }
    updateNextNode(e, t, n, o, i, s) {
        for (let r = this.index; r < this.top.children.length; r++) {
            let l = this.top.children[r];
            if (l instanceof NodeViewDesc) {
                let a = this.preMatch.matched.get(l);
                if (a != null && a != i) return false;
                let d, c = l.dom;
                let h = this.isLocked(c) && !(e.isText && l.node && l.node.isText && l.nodeDOM.nodeValue == e.text && l.dirty != xe && Ie(t, l.outerDeco));
                if (!h && l.update(e, t, n, o)) {
                    this.destroyBetween(this.index, r);
                    l.dom != c && (this.changed = true);
                    this.index++;
                    return true
                }
                if (!h && (d = this.recreateWrapper(l, e, t, n, o, s))) {
                    this.destroyBetween(this.index, r);
                    this.top.children[this.index] = d;
                    if (d.contentDOM) {
                        d.dirty = Me;
                        d.updateChildren(o, s + 1);
                        d.dirty = Oe
                    }
                    this.changed = true;
                    this.index++;
                    return true
                }
                break
            }
        }
        return false
    }
    recreateWrapper(e, t, n, o, i, s) {
        if (e.dirty || t.isAtom || !e.children.length || !e.node.content.eq(t.content) || !Ie(n, e.outerDeco) || !o.eq(e.innerDeco)) return null;
        let r = NodeViewDesc.create(this.top, t, n, o, i, s);
        if (r.contentDOM) {
            r.children = e.children;
            e.children = [];
            for (let e of r.children) e.parent = r
        }
        e.destroy();
        return r
    }
    addNode(e, t, n, o, i) {
        let s = NodeViewDesc.create(this.top, e, t, n, o, i);
        s.contentDOM && s.updateChildren(o, i + 1);
        this.top.children.splice(this.index++, 0, s);
        this.changed = true
    }
    placeWidget(e, t, n) {
        let o = this.index < this.top.children.length ? this.top.children[this.index] : null;
        if (!o || !o.matchesWidget(e) || e != o.widget && o.widget.type.toDOM.parentNode) {
            let o = new WidgetViewDesc(this.top, e, t, n);
            this.top.children.splice(this.index++, 0, o);
            this.changed = true
        } else this.index++
    }
    addTextblockHacks() {
        let e = this.top.children[this.index - 1],
            t = this.top;
        while (e instanceof MarkViewDesc) {
            t = e;
            e = t.children[t.children.length - 1]
        }
        if (!e || !(e instanceof TextViewDesc) || /\n$/.test(e.node.text) || this.view.requiresGeckoHackNode && /\s$/.test(e.node.text)) {
            (F || z) && e && e.dom.contentEditable == "false" && this.addHackNode("IMG", t);
            this.addHackNode("BR", this.top)
        }
    }
    addHackNode(e, t) {
        if (t == this.top && this.index < t.children.length && t.children[this.index].matchesHack(e)) this.index++;
        else {
            let n = document.createElement(e);
            if (e == "IMG") {
                n.className = "ProseMirror-separator";
                n.alt = ""
            }
            e == "BR" && (n.className = "ProseMirror-trailingBreak");
            let o = new TrailingHackViewDesc(this.top, [], n, null);
            t != this.top ? t.children.push(o) : t.children.splice(this.index++, 0, o);
            this.changed = true
        }
    }
    isLocked(e) {
        return this.lock && (e == this.lock || e.nodeType == 1 && e.contains(this.lock.parentNode))
    }
}

function Le(e, t) {
    let n = t,
        o = n.children.length;
    let i = e.childCount,
        s = new Map,
        r = [];
    e: while (i > 0) {
        let l;
        for (;;)
            if (o) {
                let e = n.children[o - 1];
                if (!(e instanceof MarkViewDesc)) {
                    l = e;
                    o--;
                    break
                }
                n = e;
                o = e.children.length
            } else {
                if (n == t) break e;
                o = n.parent.children.indexOf(n);
                n = n.parent
            } let a = l.node;
        if (a) {
            if (a != e.child(i - 1)) break;
            --i;
            s.set(l, i);
            r.push(l)
        }
    }
    return {
        index: i,
        matched: s,
        matches: r.reverse()
    }
}

function Fe(e, t) {
    return e.type.side - t.type.side
}

function $e(e, t, n, o) {
    let i = t.locals(e),
        s = 0;
    if (i.length == 0) {
        for (let n = 0; n < e.childCount; n++) {
            let r = e.child(n);
            o(r, i, t.forChild(s, r), n);
            s += r.nodeSize
        }
        return
    }
    let r = 0,
        l = [],
        a = null;
    for (let d = 0;;) {
        let c, h;
        while (r < i.length && i[r].to == s) {
            let e = i[r++];
            e.widget && (c ? (h || (h = [c])).push(e) : c = e)
        }
        if (c)
            if (h) {
                h.sort(Fe);
                for (let e = 0; e < h.length; e++) n(h[e], d, !!a)
            } else n(c, d, !!a);
        let f, u;
        if (a) {
            u = -1;
            f = a;
            a = null
        } else {
            if (!(d < e.childCount)) break;
            u = d;
            f = e.child(d++)
        }
        for (let e = 0; e < l.length; e++) l[e].to <= s && l.splice(e--, 1);
        while (r < i.length && i[r].from <= s && i[r].to > s) l.push(i[r++]);
        let p = s + f.nodeSize;
        if (f.isText) {
            let e = p;
            r < i.length && i[r].from < e && (e = i[r].from);
            for (let t = 0; t < l.length; t++) l[t].to < e && (e = l[t].to);
            if (e < p) {
                a = f.cut(e - s);
                f = f.cut(0, e - s);
                p = e;
                u = -1
            }
        } else
            while (r < i.length && i[r].to < p) r++;
        let m = f.isInline && !f.isLeaf ? l.filter((e => !e.inline)) : l.slice();
        o(f, m, t.forChild(s, f), u);
        s = p
    }
}

function qe(e) {
    if (e.nodeName == "UL" || e.nodeName == "OL") {
        let t = e.style.cssText;
        e.style.cssText = t + "; list-style: square !important";
        window.getComputedStyle(e).listStyle;
        e.style.cssText = t
    }
}

function Ke(e, t, n, o) {
    for (let i = 0, s = 0; i < e.childCount && s <= o;) {
        let r = e.child(i++),
            l = s;
        s += r.nodeSize;
        if (!r.isText) continue;
        let a = r.text;
        while (i < e.childCount) {
            let t = e.child(i++);
            s += t.nodeSize;
            if (!t.isText) break;
            a += t.text
        }
        if (s >= n) {
            if (s >= o && a.slice(o - t.length - l, o - l) == t) return o - t.length;
            let e = l < o ? a.lastIndexOf(t, o - l - 1) : -1;
            if (e >= 0 && e + t.length + l >= n) return l + e;
            if (n == o && a.length >= o + t.length - l && a.slice(o - l, o - l + t.length) == t) return o
        }
    }
    return -1
}

function We(e, t, n, o, i) {
    let s = [];
    for (let r = 0, l = 0; r < e.length; r++) {
        let a = e[r],
            d = l,
            c = l += a.size;
        if (d >= n || c <= t) s.push(a);
        else {
            d < t && s.push(a.slice(0, t - d, o));
            if (i) {
                s.push(i);
                i = void 0
            }
            c > n && s.push(a.slice(n - d, a.size, o))
        }
    }
    return s
}

function He(e, n = null) {
    let o = e.domSelectionRange(),
        i = e.state.doc;
    if (!o.focusNode) return null;
    let s = e.docView.nearestDesc(o.focusNode),
        r = s && s.size == 0;
    let l = e.docView.posFromDOM(o.focusNode, o.focusOffset, 1);
    if (l < 0) return null;
    let a, d, c = i.resolve(l);
    if (S(o)) {
        a = l;
        while (s && !s.node) s = s.parent;
        let e = s.node;
        if (s && e.isAtom && t.isSelectable(e) && s.parent && !(e.isInline && v(o.focusNode, o.focusOffset, s.dom))) {
            let e = s.posBefore;
            d = new t(l == e ? c : i.resolve(e))
        }
    } else {
        if (o instanceof e.dom.ownerDocument.defaultView.Selection && o.rangeCount > 1) {
            let t = l,
                n = l;
            for (let i = 0; i < o.rangeCount; i++) {
                let s = o.getRangeAt(i);
                t = Math.min(t, e.docView.posFromDOM(s.startContainer, s.startOffset, 1));
                n = Math.max(n, e.docView.posFromDOM(s.endContainer, s.endOffset, -1))
            }
            if (t < 0) return null;
            [a, l] = n == e.state.selection.anchor ? [n, t] : [t, n];
            c = i.resolve(l)
        } else a = e.docView.posFromDOM(o.anchorNode, o.anchorOffset, 1);
        if (a < 0) return null
    }
    let h = i.resolve(a);
    if (!d) {
        let t = n == "pointer" || e.state.selection.head < c.pos && !r ? 1 : -1;
        d = tt(e, h, c, t)
    }
    return d
}

function _e(e) {
    return e.editable ? e.hasFocus() : ot(e) && document.activeElement && document.activeElement.contains(e.dom)
}

function Ge(t, n = false) {
    let o = t.state.selection;
    Ze(t, o);
    if (_e(t)) {
        if (!n && t.input.mouseDown && t.input.mouseDown.allowDefault && z) {
            let e = t.domSelectionRange(),
                n = t.domObserver.currentSelection;
            if (e.anchorNode && n.anchorNode && m(e.anchorNode, e.anchorOffset, n.anchorNode, n.anchorOffset)) {
                t.input.mouseDown.delayedSelectionSync = true;
                t.domObserver.setCurSelection();
                return
            }
        }
        t.domObserver.disconnectSelection();
        if (t.cursorWrapper) Qe(t);
        else {
            let i, s, {
                anchor: r,
                head: l
            } = o;
            if (Ue && !(o instanceof e)) {
                o.$from.parent.inlineContent || (i = je(t, o.from));
                o.empty || o.$from.parent.inlineContent || (s = je(t, o.to))
            }
            t.docView.setSelection(r, l, t, n);
            if (Ue) {
                i && Ye(i);
                s && Ye(s)
            }
            if (o.visible) t.dom.classList.remove("ProseMirror-hideselection");
            else {
                t.dom.classList.add("ProseMirror-hideselection");
                "onselectionchange" in document && Je(t)
            }
        }
        t.domObserver.setCurSelection();
        t.domObserver.connectSelection()
    }
}
const Ue = F || z && L < 63;

function je(e, t) {
    let {
        node: n,
        offset: o
    } = e.docView.domFromPos(t, 0);
    let i = o < n.childNodes.length ? n.childNodes[o] : null;
    let s = o ? n.childNodes[o - 1] : null;
    if (F && i && i.contentEditable == "false") return Xe(i);
    if ((!i || i.contentEditable == "false") && (!s || s.contentEditable == "false")) {
        if (i) return Xe(i);
        if (s) return Xe(s)
    }
}

function Xe(e) {
    e.contentEditable = "true";
    if (F && e.draggable) {
        e.draggable = false;
        e.wasDraggable = true
    }
    return e
}

function Ye(e) {
    e.contentEditable = "false";
    if (e.wasDraggable) {
        e.draggable = true;
        e.wasDraggable = null
    }
}

function Je(e) {
    let t = e.dom.ownerDocument;
    t.removeEventListener("selectionchange", e.input.hideSelectionGuard);
    let n = e.domSelectionRange();
    let o = n.anchorNode,
        i = n.anchorOffset;
    t.addEventListener("selectionchange", e.input.hideSelectionGuard = () => {
        if (n.anchorNode != o || n.anchorOffset != i) {
            t.removeEventListener("selectionchange", e.input.hideSelectionGuard);
            setTimeout((() => {
                _e(e) && !e.state.selection.visible || e.dom.classList.remove("ProseMirror-hideselection")
            }), 20)
        }
    })
}

function Qe(e) {
    let t = e.domSelection(),
        n = document.createRange();
    if (!t) return;
    let o = e.cursorWrapper.dom,
        i = o.nodeName == "IMG";
    i ? n.setStart(o.parentNode, c(o) + 1) : n.setStart(o, 0);
    n.collapse(true);
    t.removeAllRanges();
    t.addRange(n);
    if (!i && !e.state.selection.visible && A && R <= 11) {
        o.disabled = true;
        o.disabled = false
    }
}

function Ze(e, n) {
    if (n instanceof t) {
        let t = e.docView.descAt(n.from);
        if (t != e.lastSelectedViewDesc) {
            et(e);
            t && t.selectNode();
            e.lastSelectedViewDesc = t
        }
    } else et(e)
}

function et(e) {
    if (e.lastSelectedViewDesc) {
        e.lastSelectedViewDesc.parent && e.lastSelectedViewDesc.deselectNode();
        e.lastSelectedViewDesc = void 0
    }
}

function tt(t, n, o, i) {
    return t.someProp("createSelectionBetween", (e => e(t, n, o))) || e.between(n, o, i)
}

function nt(e) {
    return !(e.editable && !e.hasFocus()) && ot(e)
}

function ot(e) {
    let t = e.domSelectionRange();
    if (!t.anchorNode) return false;
    try {
        return e.dom.contains(t.anchorNode.nodeType == 3 ? t.anchorNode.parentNode : t.anchorNode) && (e.editable || e.dom.contains(t.focusNode.nodeType == 3 ? t.focusNode.parentNode : t.focusNode))
    } catch (e) {
        return false
    }
}

function it(e) {
    let t = e.docView.domFromPos(e.state.selection.anchor, 0);
    let n = e.domSelectionRange();
    return m(t.node, t.offset, n.anchorNode, n.anchorOffset)
}

function st(e, t) {
    let {
        $anchor: o,
        $head: i
    } = e.selection;
    let s = t > 0 ? o.max(i) : o.min(i);
    let r = s.parent.inlineContent ? s.depth ? e.doc.resolve(t > 0 ? s.after() : s.before()) : null : s;
    return r && n.findFrom(r, t)
}

function rt(e, t) {
    e.dispatch(e.state.tr.setSelection(t).scrollIntoView());
    return true
}

function lt(n, o, i) {
    let s = n.state.selection;
    if (!(s instanceof e)) {
        if (s instanceof t && s.node.isInline) return rt(n, new e(o > 0 ? s.$to : s.$from));
        {
            let e = st(n.state, o);
            return !!e && rt(n, e)
        }
    }
    if (i.indexOf("s") > -1) {
        let {
            $head: t
        } = s, i = t.textOffset ? null : o < 0 ? t.nodeBefore : t.nodeAfter;
        if (!i || i.isText || !i.isLeaf) return false;
        let r = n.state.doc.resolve(t.pos + i.nodeSize * (o < 0 ? -1 : 1));
        return rt(n, new e(s.$anchor, r))
    }
    if (!s.empty) return false;
    if (n.endOfTextblock(o > 0 ? "forward" : "backward")) {
        let e = st(n.state, o);
        return !!(e && e instanceof t) && rt(n, e)
    }
    if (!(q && i.indexOf("m") > -1)) {
        let i, r = s.$head,
            l = r.textOffset ? null : o < 0 ? r.nodeBefore : r.nodeAfter;
        if (!l || l.isText) return false;
        let a = o < 0 ? r.pos - l.nodeSize : r.pos;
        return !!(l.isAtom || (i = n.docView.descAt(a)) && !i.contentDOM) && (t.isSelectable(l) ? rt(n, new t(o < 0 ? n.state.doc.resolve(r.pos - l.nodeSize) : r)) : !!H && rt(n, new e(n.state.doc.resolve(o < 0 ? a : a + l.nodeSize))))
    }
}

function at(e) {
    return e.nodeType == 3 ? e.nodeValue.length : e.childNodes.length
}

function dt(e, t) {
    let n = e.pmViewDesc;
    return n && n.size == 0 && (t < 0 || e.nextSibling || e.nodeName != "BR")
}

function ct(e, t) {
    return t < 0 ? ht(e) : ft(e)
}

function ht(e) {
    let t = e.domSelectionRange();
    let n = t.focusNode,
        o = t.focusOffset;
    if (!n) return;
    let i, s, r = false;
    B && n.nodeType == 1 && o < at(n) && dt(n.childNodes[o], -1) && (r = true);
    for (;;)
        if (o > 0) {
            if (n.nodeType != 1) break;
            {
                let e = n.childNodes[o - 1];
                if (dt(e, -1)) {
                    i = n;
                    s = --o
                } else {
                    if (e.nodeType != 3) break;
                    n = e;
                    o = n.nodeValue.length
                }
            }
        } else {
            if (ut(n)) break;
            {
                let t = n.previousSibling;
                while (t && dt(t, -1)) {
                    i = n.parentNode;
                    s = c(t);
                    t = t.previousSibling
                }
                if (t) {
                    n = t;
                    o = at(n)
                } else {
                    n = n.parentNode;
                    if (n == e.dom) break;
                    o = 0
                }
            }
        } r ? gt(e, n, o) : i && gt(e, i, s)
}

function ft(e) {
    let t = e.domSelectionRange();
    let n = t.focusNode,
        o = t.focusOffset;
    if (!n) return;
    let i = at(n);
    let s, r;
    for (;;)
        if (o < i) {
            if (n.nodeType != 1) break;
            let e = n.childNodes[o];
            if (!dt(e, 1)) break;
            s = n;
            r = ++o
        } else {
            if (ut(n)) break;
            {
                let t = n.nextSibling;
                while (t && dt(t, 1)) {
                    s = t.parentNode;
                    r = c(t) + 1;
                    t = t.nextSibling
                }
                if (t) {
                    n = t;
                    o = 0;
                    i = at(n)
                } else {
                    n = n.parentNode;
                    if (n == e.dom) break;
                    o = i = 0
                }
            }
        } s && gt(e, s, r)
}

function ut(e) {
    let t = e.pmViewDesc;
    return t && t.node && t.node.isBlock
}

function pt(e, t) {
    while (e && t == e.childNodes.length && !N(e)) {
        t = c(e) + 1;
        e = e.parentNode
    }
    while (e && t < e.childNodes.length) {
        let n = e.childNodes[t];
        if (n.nodeType == 3) return n;
        if (n.nodeType == 1 && n.contentEditable == "false") break;
        e = n;
        t = 0
    }
}

function mt(e, t) {
    while (e && !t && !N(e)) {
        t = c(e);
        e = e.parentNode
    }
    while (e && t) {
        let n = e.childNodes[t - 1];
        if (n.nodeType == 3) return n;
        if (n.nodeType == 1 && n.contentEditable == "false") break;
        e = n;
        t = e.childNodes.length
    }
}

function gt(e, t, n) {
    if (t.nodeType != 3) {
        let e, o;
        if (o = pt(t, n)) {
            t = o;
            n = 0
        } else if (e = mt(t, n)) {
            t = e;
            n = e.nodeValue.length
        }
    }
    let o = e.domSelection();
    if (!o) return;
    if (S(o)) {
        let e = document.createRange();
        e.setEnd(t, n);
        e.setStart(t, n);
        o.removeAllRanges();
        o.addRange(e)
    } else o.extend && o.extend(t, n);
    e.domObserver.setCurSelection();
    let {
        state: i
    } = e;
    setTimeout((() => {
        e.state == i && Ge(e)
    }), 50)
}

function yt(e, t) {
    let n = e.state.doc.resolve(t);
    if (!(z || K) && n.parent.inlineContent) {
        let o = e.coordsAtPos(t);
        if (t > n.start()) {
            let n = e.coordsAtPos(t - 1);
            let i = (n.top + n.bottom) / 2;
            if (i > o.top && i < o.bottom && Math.abs(n.left - o.left) > 1) return n.left < o.left ? "ltr" : "rtl"
        }
        if (t < n.end()) {
            let n = e.coordsAtPos(t + 1);
            let i = (n.top + n.bottom) / 2;
            if (i > o.top && i < o.bottom && Math.abs(n.left - o.left) > 1) return n.left > o.left ? "ltr" : "rtl"
        }
    }
    let o = getComputedStyle(e.dom).direction;
    return o == "rtl" ? "rtl" : "ltr"
}

function wt(i, s, r) {
    let l = i.state.selection;
    if (l instanceof e && !l.empty || r.indexOf("s") > -1) return false;
    if (q && r.indexOf("m") > -1) return false;
    let {
        $from: a,
        $to: d
    } = l;
    if (!a.parent.inlineContent || i.endOfTextblock(s < 0 ? "up" : "down")) {
        let e = st(i.state, s);
        if (e && e instanceof t) return rt(i, e)
    }
    if (!a.parent.inlineContent) {
        let e = s < 0 ? a : d;
        let t = l instanceof o ? n.near(e, s) : n.findFrom(e, s);
        return !!t && rt(i, t)
    }
    return false
}

function bt(t, n) {
    if (!(t.state.selection instanceof e)) return true;
    let {
        $head: o,
        $anchor: i,
        empty: s
    } = t.state.selection;
    if (!o.sameParent(i)) return true;
    if (!s) return false;
    if (t.endOfTextblock(n > 0 ? "forward" : "backward")) return true;
    let r = !o.textOffset && (n < 0 ? o.nodeBefore : o.nodeAfter);
    if (r && !r.isText) {
        let e = t.state.tr;
        n < 0 ? e.delete(o.pos - r.nodeSize, o.pos) : e.delete(o.pos, o.pos + r.nodeSize);
        t.dispatch(e);
        return true
    }
    return false
}

function Dt(e, t, n) {
    e.domObserver.stop();
    t.contentEditable = n;
    e.domObserver.start()
}

function vt(e) {
    if (!F || e.state.selection.$head.parentOffset > 0) return false;
    let {
        focusNode: t,
        focusOffset: n
    } = e.domSelectionRange();
    if (t && t.nodeType == 1 && n == 0 && t.firstChild && t.firstChild.contentEditable == "false") {
        let n = t.firstChild;
        Dt(e, n, "true");
        setTimeout((() => Dt(e, n, "false")), 20)
    }
    return false
}

function Nt(e) {
    let t = "";
    e.ctrlKey && (t += "c");
    e.metaKey && (t += "m");
    e.altKey && (t += "a");
    e.shiftKey && (t += "s");
    return t
}

function St(e, t) {
    let n = t.keyCode,
        o = Nt(t);
    if (n == 8 || q && n == 72 && o == "c") return bt(e, -1) || ct(e, -1);
    if (n == 46 && !t.shiftKey || q && n == 68 && o == "c") return bt(e, 1) || ct(e, 1);
    if (n == 13 || n == 27) return true;
    if (n == 37 || q && n == 66 && o == "c") {
        let t = n == 37 ? yt(e, e.state.selection.from) == "ltr" ? -1 : 1 : -1;
        return lt(e, t, o) || ct(e, t)
    }
    if (n == 39 || q && n == 70 && o == "c") {
        let t = n == 39 ? yt(e, e.state.selection.from) == "ltr" ? 1 : -1 : 1;
        return lt(e, t, o) || ct(e, t)
    }
    return n == 38 || q && n == 80 && o == "c" ? wt(e, -1, o) || ct(e, -1) : n == 40 || q && n == 78 && o == "c" ? vt(e) || wt(e, 1, o) || ct(e, 1) : o == (q ? "m" : "c") && (n == 66 || n == 73 || n == 89 || n == 90)
}

function Ot(e, t) {
    e.someProp("transformCopied", (n => {
        t = n(t, e)
    }));
    let n = [],
        {
            content: o,
            openStart: s,
            openEnd: r
        } = t;
    while (s > 1 && r > 1 && o.childCount == 1 && o.firstChild.childCount == 1) {
        s--;
        r--;
        let e = o.firstChild;
        n.push(e.type.name, e.attrs != e.type.defaultAttrs ? e.attrs : null);
        o = e.content
    }
    let l = e.someProp("clipboardSerializer") || i.fromSchema(e.state.schema);
    let a = Bt(),
        d = a.createElement("div");
    d.appendChild(l.serializeFragment(o, {
        document: a
    }));
    let c, h = d.firstChild,
        f = 0;
    while (h && h.nodeType == 1 && (c = At[h.nodeName.toLowerCase()])) {
        for (let e = c.length - 1; e >= 0; e--) {
            let t = a.createElement(c[e]);
            while (d.firstChild) t.appendChild(d.firstChild);
            d.appendChild(t);
            f++
        }
        h = d.firstChild
    }
    h && h.nodeType == 1 && h.setAttribute("data-pm-slice", `${s} ${r}${f?` -${f}`:""} ${JSON.stringify(n)}`);
    let u = e.someProp("clipboardTextSerializer", (n => n(t, e))) || t.content.textBetween(0, t.content.size, "\n\n");
    return {
        dom: d,
        text: u,
        slice: t
    }
}

function Ct(e, t, n, o, r) {
    let d = r.parent.type.spec.code;
    let c, h;
    if (!n && !t) return null;
    let f = t && (o || d || !n);
    if (f) {
        e.someProp("transformPastedText", (n => {
            t = n(t, d || o, e)
        }));
        if (d) return t ? new l(s.from(e.state.schema.text(t.replace(/\r\n?/g, "\n"))), 0, 0) : l.empty;
        let n = e.someProp("clipboardTextParser", (n => n(t, r, o, e)));
        if (n) h = n;
        else {
            let n = r.marks();
            let {
                schema: o
            } = e.state, s = i.fromSchema(o);
            c = document.createElement("div");
            t.split(/(?:\r\n?|\n)+/).forEach((e => {
                let t = c.appendChild(document.createElement("p"));
                e && t.appendChild(s.serializeNode(o.text(e, n)))
            }))
        }
    } else {
        e.someProp("transformPastedHTML", (t => {
            n = t(n, e)
        }));
        c = Lt(n);
        H && Ft(c)
    }
    let u = c && c.querySelector("[data-pm-slice]");
    let p = u && /^(\d+) (\d+)(?: -(\d+))? (.*)/.exec(u.getAttribute("data-pm-slice") || "");
    if (p && p[3])
        for (let e = +p[3]; e > 0; e--) {
            let e = c.firstChild;
            while (e && e.nodeType != 1) e = e.nextSibling;
            if (!e) break;
            c = e
        }
    if (!h) {
        let t = e.someProp("clipboardParser") || e.someProp("domParser") || a.fromSchema(e.state.schema);
        h = t.parseSlice(c, {
            preserveWhitespace: !!(f || p),
            context: r,
            ruleFromNode(e) {
                return e.nodeName != "BR" || e.nextSibling || !e.parentNode || Mt.test(e.parentNode.nodeName) ? null : {
                    ignore: true
                }
            }
        })
    }
    if (p) h = $t(Pt(h, +p[1], +p[2]), p[4]);
    else {
        h = l.maxOpen(xt(h.content, r), true);
        if (h.openStart || h.openEnd) {
            let e = 0,
                t = 0;
            for (let t = h.content.firstChild; e < h.openStart && !t.type.spec.isolating; e++, t = t.firstChild);
            for (let e = h.content.lastChild; t < h.openEnd && !e.type.spec.isolating; t++, e = e.lastChild);
            h = Pt(h, e, t)
        }
    }
    e.someProp("transformPasted", (t => {
        h = t(h, e)
    }));
    return h
}
const Mt = /^(a|abbr|acronym|b|cite|code|del|em|i|ins|kbd|label|output|q|ruby|s|samp|span|strong|sub|sup|time|u|tt|var)$/i;

function xt(e, t) {
    if (e.childCount < 2) return e;
    for (let n = t.depth; n >= 0; n--) {
        let o = t.node(n);
        let i = o.contentMatchAt(t.index(n));
        let r, l = [];
        e.forEach((e => {
            if (!l) return;
            let t, n = i.findWrapping(e.type);
            if (!n) return l = null;
            if (t = l.length && r.length && kt(n, r, e, l[l.length - 1], 0)) l[l.length - 1] = t;
            else {
                l.length && (l[l.length - 1] = Vt(l[l.length - 1], r.length));
                let t = Tt(e, n);
                l.push(t);
                i = i.matchType(t.type);
                r = n
            }
        }));
        if (l) return s.from(l)
    }
    return e
}

function Tt(e, t, n = 0) {
    for (let o = t.length - 1; o >= n; o--) e = t[o].create(null, s.from(e));
    return e
}

function kt(e, t, n, o, i) {
    if (i < e.length && i < t.length && e[i] == t[i]) {
        let r = kt(e, t, n, o.lastChild, i + 1);
        if (r) return o.copy(o.content.replaceChild(o.childCount - 1, r));
        let l = o.contentMatchAt(o.childCount);
        if (l.matchType(i == e.length - 1 ? n.type : e[i + 1])) return o.copy(o.content.append(s.from(Tt(n, e, i + 1))))
    }
}

function Vt(e, t) {
    if (t == 0) return e;
    let n = e.content.replaceChild(e.childCount - 1, Vt(e.lastChild, t - 1));
    let o = e.contentMatchAt(e.childCount).fillBefore(s.empty, true);
    return e.copy(n.append(o))
}

function Et(e, t, n, o, i, r) {
    let l = t < 0 ? e.firstChild : e.lastChild,
        a = l.content;
    e.childCount > 1 && (r = 0);
    i < o - 1 && (a = Et(a, t, n, o, i + 1, r));
    i >= n && (a = t < 0 ? l.contentMatchAt(0).fillBefore(a, r <= i).append(a) : a.append(l.contentMatchAt(l.childCount).fillBefore(s.empty, true)));
    return e.replaceChild(t < 0 ? 0 : e.childCount - 1, l.copy(a))
}

function Pt(e, t, n) {
    t < e.openStart && (e = new l(Et(e.content, -1, t, e.openStart, 0, e.openEnd), t, e.openEnd));
    n < e.openEnd && (e = new l(Et(e.content, 1, n, e.openEnd, 0, 0), e.openStart, n));
    return e
}
const At = {
    thead: ["table"],
    tbody: ["table"],
    tfoot: ["table"],
    caption: ["table"],
    colgroup: ["table"],
    col: ["table", "colgroup"],
    tr: ["table", "tbody"],
    td: ["table", "tbody", "tr"],
    th: ["table", "tbody", "tr"]
};
let Rt = null;

function Bt() {
    return Rt || (Rt = document.implementation.createHTMLDocument("title"))
}
let It = null;

function zt(e) {
    let t = window.trustedTypes;
    if (!t) return e;
    It || (It = t.defaultPolicy || t.createPolicy("ProseMirrorClipboard", {
        createHTML: e => e
    }));
    return It.createHTML(e)
}

function Lt(e) {
    let t = /^(\s*<meta [^>]*>)*/.exec(e);
    t && (e = e.slice(t[0].length));
    let n = Bt().createElement("div");
    let o, i = /<([a-z][^>\s]+)/i.exec(e);
    (o = i && At[i[1].toLowerCase()]) && (e = o.map((e => "<" + e + ">")).join("") + e + o.map((e => "</" + e + ">")).reverse().join(""));
    n.innerHTML = zt(e);
    if (o)
        for (let e = 0; e < o.length; e++) n = n.querySelector(o[e]) || n;
    return n
}

function Ft(e) {
    let t = e.querySelectorAll(z ? "span:not([class]):not([style])" : "span.Apple-converted-space");
    for (let n = 0; n < t.length; n++) {
        let o = t[n];
        o.childNodes.length == 1 && o.textContent == " " && o.parentNode && o.parentNode.replaceChild(e.ownerDocument.createTextNode(" "), o)
    }
}

function $t(e, t) {
    if (!e.size) return e;
    let n, o = e.content.firstChild.type.schema;
    try {
        n = JSON.parse(t)
    } catch (t) {
        return e
    }
    let {
        content: i,
        openStart: r,
        openEnd: a
    } = e;
    for (let e = n.length - 2; e >= 0; e -= 2) {
        let t = o.nodes[n[e]];
        if (!t || t.hasRequiredAttrs()) break;
        i = s.from(t.create(n[e + 1], i));
        r++;
        a++
    }
    return new l(i, r, a)
}
const qt = {};
const Kt = {};
const Wt = {
    touchstart: true,
    touchmove: true
};
class InputState {
    constructor() {
        this.shiftKey = false;
        this.mouseDown = null;
        this.lastKeyCode = null;
        this.lastKeyCodeTime = 0;
        this.lastClick = {
            time: 0,
            x: 0,
            y: 0,
            type: "",
            button: 0
        };
        this.lastSelectionOrigin = null;
        this.lastSelectionTime = 0;
        this.lastIOSEnter = 0;
        this.lastIOSEnterFallbackTimeout = -1;
        this.lastFocus = 0;
        this.lastTouch = 0;
        this.lastChromeDelete = 0;
        this.composing = false;
        this.compositionNode = null;
        this.composingTimeout = -1;
        this.compositionNodes = [];
        this.compositionEndedAt = -2e8;
        this.compositionID = 1;
        this.compositionPendingChanges = 0;
        this.domChangeCount = 0;
        this.eventHandlers = Object.create(null);
        this.hideSelectionGuard = null
    }
}

function Ht(e) {
    for (let t in qt) {
        let n = qt[t];
        e.dom.addEventListener(t, e.input.eventHandlers[t] = t => {
            !Xt(e, t) || jt(e, t) || !e.editable && t.type in Kt || n(e, t)
        }, Wt[t] ? {
            passive: true
        } : void 0)
    }
    F && e.dom.addEventListener("input", (() => null));
    Ut(e)
}

function _t(e, t) {
    e.input.lastSelectionOrigin = t;
    e.input.lastSelectionTime = Date.now()
}

function Gt(e) {
    e.domObserver.stop();
    for (let t in e.input.eventHandlers) e.dom.removeEventListener(t, e.input.eventHandlers[t]);
    clearTimeout(e.input.composingTimeout);
    clearTimeout(e.input.lastIOSEnterFallbackTimeout)
}

function Ut(e) {
    e.someProp("handleDOMEvents", (t => {
        for (let n in t) e.input.eventHandlers[n] || e.dom.addEventListener(n, e.input.eventHandlers[n] = t => jt(e, t))
    }))
}

function jt(e, t) {
    return e.someProp("handleDOMEvents", (n => {
        let o = n[t.type];
        return !!o && (o(e, t) || t.defaultPrevented)
    }))
}

function Xt(e, t) {
    if (!t.bubbles) return true;
    if (t.defaultPrevented) return false;
    for (let n = t.target; n != e.dom; n = n.parentNode)
        if (!n || n.nodeType == 11 || n.pmViewDesc && n.pmViewDesc.stopEvent(t)) return false;
    return true
}

function Yt(e, t) {
    jt(e, t) || !qt[t.type] || !e.editable && t.type in Kt || qt[t.type](e, t)
}
Kt.keydown = (e, t) => {
    let n = t;
    e.input.shiftKey = n.keyCode == 16 || n.shiftKey;
    if (!cn(e, n)) {
        e.input.lastKeyCode = n.keyCode;
        e.input.lastKeyCodeTime = Date.now();
        if (!W || !z || n.keyCode != 13) {
            n.keyCode != 229 && e.domObserver.forceFlush();
            if (!$ || n.keyCode != 13 || n.ctrlKey || n.altKey || n.metaKey) e.someProp("handleKeyDown", (t => t(e, n))) || St(e, n) ? n.preventDefault() : _t(e, "key");
            else {
                let t = Date.now();
                e.input.lastIOSEnter = t;
                e.input.lastIOSEnterFallbackTimeout = setTimeout((() => {
                    if (e.input.lastIOSEnter == t) {
                        e.someProp("handleKeyDown", (t => t(e, O(13, "Enter"))));
                        e.input.lastIOSEnter = 0
                    }
                }), 200)
            }
        }
    }
};
Kt.keyup = (e, t) => {
    t.keyCode == 16 && (e.input.shiftKey = false)
};
Kt.keypress = (t, n) => {
    let o = n;
    if (cn(t, o) || !o.charCode || o.ctrlKey && !o.altKey || q && o.metaKey) return;
    if (t.someProp("handleKeyPress", (e => e(t, o)))) {
        o.preventDefault();
        return
    }
    let i = t.state.selection;
    if (!(i instanceof e) || !i.$from.sameParent(i.$to)) {
        let e = String.fromCharCode(o.charCode);
        /[\r\n]/.test(e) || t.someProp("handleTextInput", (n => n(t, i.$from.pos, i.$to.pos, e))) || t.dispatch(t.state.tr.insertText(e).scrollIntoView());
        o.preventDefault()
    }
};

function Jt(e) {
    return {
        left: e.clientX,
        top: e.clientY
    }
}

function Qt(e, t) {
    let n = t.x - e.clientX,
        o = t.y - e.clientY;
    return n * n + o * o < 100
}

function Zt(e, t, n, o, i) {
    if (o == -1) return false;
    let s = e.state.doc.resolve(o);
    for (let o = s.depth + 1; o > 0; o--)
        if (e.someProp(t, (t => o > s.depth ? t(e, n, s.nodeAfter, s.before(o), i, true) : t(e, n, s.node(o), s.before(o), i, false)))) return true;
    return false
}

function en(e, t, n) {
    e.focused || e.focus();
    if (e.state.selection.eq(t)) return;
    let o = e.state.tr.setSelection(t);
    n == "pointer" && o.setMeta("pointer", true);
    e.dispatch(o)
}

function tn(e, n) {
    if (n == -1) return false;
    let o = e.state.doc.resolve(n),
        i = o.nodeAfter;
    if (i && i.isAtom && t.isSelectable(i)) {
        en(e, new t(o), "pointer");
        return true
    }
    return false
}

function nn(e, n) {
    if (n == -1) return false;
    let o, i, s = e.state.selection;
    s instanceof t && (o = s.node);
    let r = e.state.doc.resolve(n);
    for (let e = r.depth + 1; e > 0; e--) {
        let n = e > r.depth ? r.nodeAfter : r.node(e);
        if (t.isSelectable(n)) {
            i = o && s.$from.depth > 0 && e >= s.$from.depth && r.before(s.$from.depth + 1) == s.$from.pos ? r.before(s.$from.depth) : r.before(e);
            break
        }
    }
    if (i != null) {
        en(e, t.create(e.state.doc, i), "pointer");
        return true
    }
    return false
}

function on(e, t, n, o, i) {
    return Zt(e, "handleClickOn", t, n, o) || e.someProp("handleClick", (n => n(e, t, o))) || (i ? nn(e, n) : tn(e, n))
}

function sn(e, t, n, o) {
    return Zt(e, "handleDoubleClickOn", t, n, o) || e.someProp("handleDoubleClick", (n => n(e, t, o)))
}

function rn(e, t, n, o) {
    return Zt(e, "handleTripleClickOn", t, n, o) || e.someProp("handleTripleClick", (n => n(e, t, o))) || ln(e, n, o)
}

function ln(n, o, i) {
    if (i.button != 0) return false;
    let s = n.state.doc;
    if (o == -1) {
        if (s.inlineContent) {
            en(n, e.create(s, 0, s.content.size), "pointer");
            return true
        }
        return false
    }
    let r = s.resolve(o);
    for (let o = r.depth + 1; o > 0; o--) {
        let i = o > r.depth ? r.nodeAfter : r.node(o);
        let l = r.before(o);
        if (i.inlineContent) en(n, e.create(s, l + 1, l + 1 + i.content.size), "pointer");
        else {
            if (!t.isSelectable(i)) continue;
            en(n, t.create(s, l), "pointer")
        }
        return true
    }
}

function an(e) {
    return gn(e)
}
const dn = q ? "metaKey" : "ctrlKey";
qt.mousedown = (e, t) => {
    let n = t;
    e.input.shiftKey = n.shiftKey;
    let o = an(e);
    let i = Date.now(),
        s = "singleClick";
    i - e.input.lastClick.time < 500 && Qt(n, e.input.lastClick) && !n[dn] && e.input.lastClick.button == n.button && (e.input.lastClick.type == "singleClick" ? s = "doubleClick" : e.input.lastClick.type == "doubleClick" && (s = "tripleClick"));
    e.input.lastClick = {
        time: i,
        x: n.clientX,
        y: n.clientY,
        type: s,
        button: n.button
    };
    let r = e.posAtCoords(Jt(n));
    if (r)
        if (s == "singleClick") {
            e.input.mouseDown && e.input.mouseDown.done();
            e.input.mouseDown = new MouseDown(e, r, n, !!o)
        } else(s == "doubleClick" ? sn : rn)(e, r.pos, r.inside, n) ? n.preventDefault() : _t(e, "pointer")
};
class MouseDown {
    constructor(e, n, o, i) {
        this.view = e;
        this.pos = n;
        this.event = o;
        this.flushed = i;
        this.delayedSelectionSync = false;
        this.mightDrag = null;
        this.startDoc = e.state.doc;
        this.selectNode = !!o[dn];
        this.allowDefault = o.shiftKey;
        let s, r;
        if (n.inside > -1) {
            s = e.state.doc.nodeAt(n.inside);
            r = n.inside
        } else {
            let t = e.state.doc.resolve(n.pos);
            s = t.parent;
            r = t.depth ? t.before() : 0
        }
        const l = i ? null : o.target;
        const a = l ? e.docView.nearestDesc(l, true) : null;
        this.target = a && a.dom.nodeType == 1 ? a.dom : null;
        let {
            selection: d
        } = e.state;
        (o.button == 0 && s.type.spec.draggable && s.type.spec.selectable !== false || d instanceof t && d.from <= r && d.to > r) && (this.mightDrag = {
            node: s,
            pos: r,
            addAttr: !!(this.target && !this.target.draggable),
            setUneditable: !!(this.target && B && !this.target.hasAttribute("contentEditable"))
        });
        if (this.target && this.mightDrag && (this.mightDrag.addAttr || this.mightDrag.setUneditable)) {
            this.view.domObserver.stop();
            this.mightDrag.addAttr && (this.target.draggable = true);
            this.mightDrag.setUneditable && setTimeout((() => {
                this.view.input.mouseDown == this && this.target.setAttribute("contentEditable", "false")
            }), 20);
            this.view.domObserver.start()
        }
        e.root.addEventListener("mouseup", this.up = this.up.bind(this));
        e.root.addEventListener("mousemove", this.move = this.move.bind(this));
        _t(e, "pointer")
    }
    done() {
        this.view.root.removeEventListener("mouseup", this.up);
        this.view.root.removeEventListener("mousemove", this.move);
        if (this.mightDrag && this.target) {
            this.view.domObserver.stop();
            this.mightDrag.addAttr && this.target.removeAttribute("draggable");
            this.mightDrag.setUneditable && this.target.removeAttribute("contentEditable");
            this.view.domObserver.start()
        }
        this.delayedSelectionSync && setTimeout((() => Ge(this.view)));
        this.view.input.mouseDown = null
    }
    up(e) {
        this.done();
        if (!this.view.dom.contains(e.target)) return;
        let t = this.pos;
        this.view.state.doc != this.startDoc && (t = this.view.posAtCoords(Jt(e)));
        this.updateAllowDefault(e);
        if (this.allowDefault || !t) _t(this.view, "pointer");
        else if (on(this.view, t.pos, t.inside, e, this.selectNode)) e.preventDefault();
        else if (e.button == 0 && (this.flushed || F && this.mightDrag && !this.mightDrag.node.isAtom || z && !this.view.state.selection.visible && Math.min(Math.abs(t.pos - this.view.state.selection.from), Math.abs(t.pos - this.view.state.selection.to)) <= 2)) {
            en(this.view, n.near(this.view.state.doc.resolve(t.pos)), "pointer");
            e.preventDefault()
        } else _t(this.view, "pointer")
    }
    move(e) {
        this.updateAllowDefault(e);
        _t(this.view, "pointer");
        e.buttons == 0 && this.done()
    }
    updateAllowDefault(e) {
        !this.allowDefault && (Math.abs(this.event.x - e.clientX) > 4 || Math.abs(this.event.y - e.clientY) > 4) && (this.allowDefault = true)
    }
}
qt.touchstart = e => {
    e.input.lastTouch = Date.now();
    an(e);
    _t(e, "pointer")
};
qt.touchmove = e => {
    e.input.lastTouch = Date.now();
    _t(e, "pointer")
};
qt.contextmenu = e => an(e);

function cn(e, t) {
    if (e.composing) return true;
    if (F && Math.abs(t.timeStamp - e.input.compositionEndedAt) < 500) {
        e.input.compositionEndedAt = -2e8;
        return true
    }
    return false
}
const hn = W ? 5e3 : -1;
Kt.compositionstart = Kt.compositionupdate = t => {
    if (!t.composing) {
        t.domObserver.flush();
        let {
            state: n
        } = t, o = n.selection.$to;
        if (n.selection instanceof e && (n.storedMarks || !o.textOffset && o.parentOffset && o.nodeBefore.marks.some((e => e.type.spec.inclusive === false)))) {
            t.markCursor = t.state.storedMarks || o.marks();
            gn(t, true);
            t.markCursor = null
        } else {
            gn(t, !n.selection.empty);
            if (B && n.selection.empty && o.parentOffset && !o.textOffset && o.nodeBefore.marks.length) {
                let e = t.domSelectionRange();
                for (let n = e.focusNode, o = e.focusOffset; n && n.nodeType == 1 && o != 0;) {
                    let e = o < 0 ? n.lastChild : n.childNodes[o - 1];
                    if (!e) break;
                    if (e.nodeType == 3) {
                        let n = t.domSelection();
                        n && n.collapse(e, e.nodeValue.length);
                        break
                    }
                    n = e;
                    o = -1
                }
            }
        }
        t.input.composing = true
    }
    fn(t, hn)
};
Kt.compositionend = (e, t) => {
    if (e.composing) {
        e.input.composing = false;
        e.input.compositionEndedAt = t.timeStamp;
        e.input.compositionPendingChanges = e.domObserver.pendingRecords().length ? e.input.compositionID : 0;
        e.input.compositionNode = null;
        e.input.compositionPendingChanges && Promise.resolve().then((() => e.domObserver.flush()));
        e.input.compositionID++;
        fn(e, 20)
    }
};

function fn(e, t) {
    clearTimeout(e.input.composingTimeout);
    t > -1 && (e.input.composingTimeout = setTimeout((() => gn(e)), t))
}

function un(e) {
    if (e.composing) {
        e.input.composing = false;
        e.input.compositionEndedAt = mn()
    }
    while (e.input.compositionNodes.length > 0) e.input.compositionNodes.pop().markParentsDirty()
}

function pn(e) {
    let t = e.domSelectionRange();
    if (!t.focusNode) return null;
    let n = b(t.focusNode, t.focusOffset);
    let o = D(t.focusNode, t.focusOffset);
    if (n && o && n != o) {
        let t = o.pmViewDesc,
            i = e.domObserver.lastChangedTextNode;
        if (n == i || o == i) return i;
        if (!t || !t.isText(o.nodeValue)) return o;
        if (e.input.compositionNode == o) {
            let e = n.pmViewDesc;
            if (!(!e || !e.isText(n.nodeValue))) return o
        }
    }
    return n || o
}

function mn() {
    let e = document.createEvent("Event");
    e.initEvent("event", true, true);
    return e.timeStamp
}

function gn(e, t = false) {
    if (!(W && e.domObserver.flushingSoon >= 0)) {
        e.domObserver.forceFlush();
        un(e);
        if (t || e.docView && e.docView.dirty) {
            let n = He(e),
                o = e.state.selection;
            n && !n.eq(o) ? e.dispatch(e.state.tr.setSelection(n)) : !e.markCursor && !t || o.$from.node(o.$from.sharedDepth(o.to)).inlineContent ? e.updateState(e.state) : e.dispatch(e.state.tr.deleteSelection());
            return true
        }
        return false
    }
}

function yn(e, t) {
    if (!e.dom.parentNode) return;
    let n = e.dom.parentNode.appendChild(document.createElement("div"));
    n.appendChild(t);
    n.style.cssText = "position: fixed; left: -10000px; top: 10px";
    let o = getSelection(),
        i = document.createRange();
    i.selectNodeContents(t);
    e.dom.blur();
    o.removeAllRanges();
    o.addRange(i);
    setTimeout((() => {
        n.parentNode && n.parentNode.removeChild(n);
        e.focus()
    }), 50)
}
const wn = A && R < 15 || $ && _ < 604;
qt.copy = Kt.cut = (e, t) => {
    let n = t;
    let o = e.state.selection,
        i = n.type == "cut";
    if (o.empty) return;
    let s = wn ? null : n.clipboardData;
    let r = o.content(),
        {
            dom: l,
            text: a
        } = Ot(e, r);
    if (s) {
        n.preventDefault();
        s.clearData();
        s.setData("text/html", l.innerHTML);
        s.setData("text/plain", a)
    } else yn(e, l);
    i && e.dispatch(e.state.tr.deleteSelection().scrollIntoView().setMeta("uiEvent", "cut"))
};

function bn(e) {
    return e.openStart == 0 && e.openEnd == 0 && e.content.childCount == 1 ? e.content.firstChild : null
}

function Dn(e, t) {
    if (!e.dom.parentNode) return;
    let n = e.input.shiftKey || e.state.selection.$from.parent.type.spec.code;
    let o = e.dom.parentNode.appendChild(document.createElement(n ? "textarea" : "div"));
    n || (o.contentEditable = "true");
    o.style.cssText = "position: fixed; left: -10000px; top: 10px";
    o.focus();
    let i = e.input.shiftKey && e.input.lastKeyCode != 45;
    setTimeout((() => {
        e.focus();
        o.parentNode && o.parentNode.removeChild(o);
        n ? vn(e, o.value, null, i, t) : vn(e, o.textContent, o.innerHTML, i, t)
    }), 50)
}

function vn(e, t, n, o, i) {
    let s = Ct(e, t, n, o, e.state.selection.$from);
    if (e.someProp("handlePaste", (t => t(e, i, s || l.empty)))) return true;
    if (!s) return false;
    let r = bn(s);
    let a = r ? e.state.tr.replaceSelectionWith(r, o) : e.state.tr.replaceSelection(s);
    e.dispatch(a.scrollIntoView().setMeta("paste", true).setMeta("uiEvent", "paste"));
    return true
}

function Nn(e) {
    let t = e.getData("text/plain") || e.getData("Text");
    if (t) return t;
    let n = e.getData("text/uri-list");
    return n ? n.replace(/\r?\n/g, " ") : ""
}
Kt.paste = (e, t) => {
    let n = t;
    if (e.composing && !W) return;
    let o = wn ? null : n.clipboardData;
    let i = e.input.shiftKey && e.input.lastKeyCode != 45;
    o && vn(e, Nn(o), o.getData("text/html"), i, n) ? n.preventDefault() : Dn(e, n)
};
class Dragging {
    constructor(e, t, n) {
        this.slice = e;
        this.move = t;
        this.node = n
    }
}
const Sn = q ? "altKey" : "ctrlKey";

function On(e, t) {
    let n = e.someProp("dragCopies", (e => !e(t)));
    return n != null ? n : !t[Sn]
}
qt.dragstart = (e, n) => {
    let o = n;
    let i = e.input.mouseDown;
    i && i.done();
    if (!o.dataTransfer) return;
    let s = e.state.selection;
    let r = s.empty ? null : e.posAtCoords(Jt(o));
    let l;
    if (r && r.pos >= s.from && r.pos <= (s instanceof t ? s.to - 1 : s.to));
    else if (i && i.mightDrag) l = t.create(e.state.doc, i.mightDrag.pos);
    else if (o.target && o.target.nodeType == 1) {
        let n = e.docView.nearestDesc(o.target, true);
        n && n.node.type.spec.draggable && n != e.docView && (l = t.create(e.state.doc, n.posBefore))
    }
    let a = (l || e.state.selection).content();
    let {
        dom: d,
        text: c,
        slice: h
    } = Ot(e, a);
    (!o.dataTransfer.files.length || !z || L > 120) && o.dataTransfer.clearData();
    o.dataTransfer.setData(wn ? "Text" : "text/html", d.innerHTML);
    o.dataTransfer.effectAllowed = "copyMove";
    wn || o.dataTransfer.setData("text/plain", c);
    e.dragging = new Dragging(h, On(e, o), l)
};
qt.dragend = e => {
    let t = e.dragging;
    window.setTimeout((() => {
        e.dragging == t && (e.dragging = null)
    }), 50)
};
Kt.dragover = Kt.dragenter = (e, t) => t.preventDefault();
Kt.drop = (e, n) => {
    let o = n;
    let i = e.dragging;
    e.dragging = null;
    if (!o.dataTransfer) return;
    let s = e.posAtCoords(Jt(o));
    if (!s) return;
    let r = e.state.doc.resolve(s.pos);
    let a = i && i.slice;
    a ? e.someProp("transformPasted", (t => {
        a = t(a, e)
    })) : a = Ct(e, Nn(o.dataTransfer), wn ? null : o.dataTransfer.getData("text/html"), false, r);
    let c = !!(i && On(e, o));
    if (e.someProp("handleDrop", (t => t(e, o, a || l.empty, c)))) {
        o.preventDefault();
        return
    }
    if (!a) return;
    o.preventDefault();
    let h = a ? d(e.state.doc, r.pos, a) : r.pos;
    h == null && (h = r.pos);
    let f = e.state.tr;
    if (c) {
        let {
            node: e
        } = i;
        e ? e.replace(f) : f.deleteSelection()
    }
    let u = f.mapping.map(h);
    let p = a.openStart == 0 && a.openEnd == 0 && a.content.childCount == 1;
    let m = f.doc;
    p ? f.replaceRangeWith(u, u, a.content.firstChild) : f.replaceRange(u, u, a);
    if (f.doc.eq(m)) return;
    let g = f.doc.resolve(u);
    if (p && t.isSelectable(a.content.firstChild) && g.nodeAfter && g.nodeAfter.sameMarkup(a.content.firstChild)) f.setSelection(new t(g));
    else {
        let t = f.mapping.map(h);
        f.mapping.maps[f.mapping.maps.length - 1].forEach(((e, n, o, i) => t = i));
        f.setSelection(tt(e, g, f.doc.resolve(t)))
    }
    e.focus();
    e.dispatch(f.setMeta("uiEvent", "drop"))
};
qt.focus = e => {
    e.input.lastFocus = Date.now();
    if (!e.focused) {
        e.domObserver.stop();
        e.dom.classList.add("ProseMirror-focused");
        e.domObserver.start();
        e.focused = true;
        setTimeout((() => {
            e.docView && e.hasFocus() && !e.domObserver.currentSelection.eq(e.domSelectionRange()) && Ge(e)
        }), 20)
    }
};
qt.blur = (e, t) => {
    let n = t;
    if (e.focused) {
        e.domObserver.stop();
        e.dom.classList.remove("ProseMirror-focused");
        e.domObserver.start();
        n.relatedTarget && e.dom.contains(n.relatedTarget) && e.domObserver.currentSelection.clear();
        e.focused = false
    }
};
qt.beforeinput = (e, t) => {
    let n = t;
    if (z && W && n.inputType == "deleteContentBackward") {
        e.domObserver.flushSoon();
        let {
            domChangeCount: t
        } = e.input;
        setTimeout((() => {
            if (e.input.domChangeCount != t) return;
            e.dom.blur();
            e.focus();
            if (e.someProp("handleKeyDown", (t => t(e, O(8, "Backspace"))))) return;
            let {
                $cursor: n
            } = e.state.selection;
            n && n.pos > 0 && e.dispatch(e.state.tr.delete(n.pos - 1, n.pos).scrollIntoView())
        }), 50)
    }
};
for (let e in Kt) qt[e] = Kt[e];

function Cn(e, t) {
    if (e == t) return true;
    for (let n in e)
        if (e[n] !== t[n]) return false;
    for (let n in t)
        if (!(n in e)) return false;
    return true
}
class WidgetType {
    constructor(e, t) {
        this.toDOM = e;
        this.spec = t || xn;
        this.side = this.spec.side || 0
    }
    map(e, t, n, o) {
        let {
            pos: i,
            deleted: s
        } = e.mapResult(t.from + o, this.side < 0 ? -1 : 1);
        return s ? null : new Decoration(i - n, i - n, this)
    }
    valid() {
        return true
    }
    eq(e) {
        return this == e || e instanceof WidgetType && (this.spec.key && this.spec.key == e.spec.key || this.toDOM == e.toDOM && Cn(this.spec, e.spec))
    }
    destroy(e) {
        this.spec.destroy && this.spec.destroy(e)
    }
}
class InlineType {
    constructor(e, t) {
        this.attrs = e;
        this.spec = t || xn
    }
    map(e, t, n, o) {
        let i = e.map(t.from + o, this.spec.inclusiveStart ? -1 : 1) - n;
        let s = e.map(t.to + o, this.spec.inclusiveEnd ? 1 : -1) - n;
        return i >= s ? null : new Decoration(i, s, this)
    }
    valid(e, t) {
        return t.from < t.to
    }
    eq(e) {
        return this == e || e instanceof InlineType && Cn(this.attrs, e.attrs) && Cn(this.spec, e.spec)
    }
    static is(e) {
        return e.type instanceof InlineType
    }
    destroy() {}
}
class NodeType {
    constructor(e, t) {
        this.attrs = e;
        this.spec = t || xn
    }
    map(e, t, n, o) {
        let i = e.mapResult(t.from + o, 1);
        if (i.deleted) return null;
        let s = e.mapResult(t.to + o, -1);
        return s.deleted || s.pos <= i.pos ? null : new Decoration(i.pos - n, s.pos - n, this)
    }
    valid(e, t) {
        let n, {
            index: o,
            offset: i
        } = e.content.findIndex(t.from);
        return i == t.from && !(n = e.child(o)).isText && i + n.nodeSize == t.to
    }
    eq(e) {
        return this == e || e instanceof NodeType && Cn(this.attrs, e.attrs) && Cn(this.spec, e.spec)
    }
    destroy() {}
}
class Decoration {
    constructor(e, t, n) {
        this.from = e;
        this.to = t;
        this.type = n
    }
    copy(e, t) {
        return new Decoration(e, t, this.type)
    }
    eq(e, t = 0) {
        return this.type.eq(e.type) && this.from + t == e.from && this.to + t == e.to
    }
    map(e, t, n) {
        return this.type.map(e, this, t, n)
    }
    static widget(e, t, n) {
        return new Decoration(e, e, new WidgetType(t, n))
    }
    static inline(e, t, n, o) {
        return new Decoration(e, t, new InlineType(n, o))
    }
    static node(e, t, n, o) {
        return new Decoration(e, t, new NodeType(n, o))
    }
    get spec() {
        return this.type.spec
    }
    get inline() {
        return this.type instanceof InlineType
    }
    get widget() {
        return this.type instanceof WidgetType
    }
}
const Mn = [],
    xn = {};
class DecorationSet {
    constructor(e, t) {
        this.local = e.length ? e : Mn;
        this.children = t.length ? t : Mn
    }
    static create(e, t) {
        return t.length ? Rn(t, e, 0, xn) : Tn
    }
    find(e, t, n) {
        let o = [];
        this.findInner(e == null ? 0 : e, t == null ? 1e9 : t, o, 0, n);
        return o
    }
    findInner(e, t, n, o, i) {
        for (let s = 0; s < this.local.length; s++) {
            let r = this.local[s];
            r.from <= t && r.to >= e && (!i || i(r.spec)) && n.push(r.copy(r.from + o, r.to + o))
        }
        for (let s = 0; s < this.children.length; s += 3)
            if (this.children[s] < t && this.children[s + 1] > e) {
                let r = this.children[s] + 1;
                this.children[s + 2].findInner(e - r, t - r, n, o + r, i)
            }
    }
    map(e, t, n) {
        return this == Tn || e.maps.length == 0 ? this : this.mapInner(e, t, 0, 0, n || xn)
    }
    mapInner(e, t, n, o, i) {
        let s;
        for (let r = 0; r < this.local.length; r++) {
            let l = this.local[r].map(e, n, o);
            l && l.type.valid(t, l) ? (s || (s = [])).push(l) : i.onRemove && i.onRemove(this.local[r].spec)
        }
        return this.children.length ? kn(this.children, s || [], e, t, n, o, i) : s ? new DecorationSet(s.sort(Bn), Mn) : Tn
    }
    add(e, t) {
        return t.length ? this == Tn ? DecorationSet.create(e, t) : this.addInner(e, t, 0) : this
    }
    addInner(e, t, n) {
        let o, i = 0;
        e.forEach(((e, s) => {
            let r, l = s + n;
            if (r = Pn(t, e, l)) {
                o || (o = this.children.slice());
                while (i < o.length && o[i] < s) i += 3;
                o[i] == s ? o[i + 2] = o[i + 2].addInner(e, r, l + 1) : o.splice(i, 0, s, s + e.nodeSize, Rn(r, e, l + 1, xn));
                i += 3
            }
        }));
        let s = Vn(i ? An(t) : t, -n);
        for (let t = 0; t < s.length; t++) s[t].type.valid(e, s[t]) || s.splice(t--, 1);
        return new DecorationSet(s.length ? this.local.concat(s).sort(Bn) : this.local, o || this.children)
    }
    remove(e) {
        return e.length == 0 || this == Tn ? this : this.removeInner(e, 0)
    }
    removeInner(e, t) {
        let n = this.children,
            o = this.local;
        for (let o = 0; o < n.length; o += 3) {
            let i;
            let s = n[o] + t,
                r = n[o + 1] + t;
            for (let t, n = 0; n < e.length; n++)
                if ((t = e[n]) && t.from > s && t.to < r) {
                    e[n] = null;
                    (i || (i = [])).push(t)
                } if (!i) continue;
            n == this.children && (n = this.children.slice());
            let l = n[o + 2].removeInner(i, s + 1);
            if (l != Tn) n[o + 2] = l;
            else {
                n.splice(o, 3);
                o -= 3
            }
        }
        if (o.length)
            for (let n, i = 0; i < e.length; i++)
                if (n = e[i])
                    for (let e = 0; e < o.length; e++)
                        if (o[e].eq(n, t)) {
                            o == this.local && (o = this.local.slice());
                            o.splice(e--, 1)
                        } return n == this.children && o == this.local ? this : o.length || n.length ? new DecorationSet(o, n) : Tn
    }
    forChild(e, t) {
        if (this == Tn) return this;
        if (t.isLeaf) return DecorationSet.empty;
        let n, o;
        for (let t = 0; t < this.children.length; t += 3)
            if (this.children[t] >= e) {
                this.children[t] == e && (n = this.children[t + 2]);
                break
            } let i = e + 1,
            s = i + t.content.size;
        for (let e = 0; e < this.local.length; e++) {
            let t = this.local[e];
            if (t.from < s && t.to > i && t.type instanceof InlineType) {
                let e = Math.max(i, t.from) - i,
                    n = Math.min(s, t.to) - i;
                e < n && (o || (o = [])).push(t.copy(e, n))
            }
        }
        if (o) {
            let e = new DecorationSet(o.sort(Bn), Mn);
            return n ? new DecorationGroup([e, n]) : e
        }
        return n || Tn
    }
    eq(e) {
        if (this == e) return true;
        if (!(e instanceof DecorationSet) || this.local.length != e.local.length || this.children.length != e.children.length) return false;
        for (let t = 0; t < this.local.length; t++)
            if (!this.local[t].eq(e.local[t])) return false;
        for (let t = 0; t < this.children.length; t += 3)
            if (this.children[t] != e.children[t] || this.children[t + 1] != e.children[t + 1] || !this.children[t + 2].eq(e.children[t + 2])) return false;
        return true
    }
    locals(e) {
        return In(this.localsInner(e))
    }
    localsInner(e) {
        if (this == Tn) return Mn;
        if (e.inlineContent || !this.local.some(InlineType.is)) return this.local;
        let t = [];
        for (let e = 0; e < this.local.length; e++) this.local[e].type instanceof InlineType || t.push(this.local[e]);
        return t
    }
    forEachSet(e) {
        e(this)
    }
}
DecorationSet.empty = new DecorationSet([], []);
DecorationSet.removeOverlap = In;
const Tn = DecorationSet.empty;
class DecorationGroup {
    constructor(e) {
        this.members = e
    }
    map(e, t) {
        const n = this.members.map((n => n.map(e, t, xn)));
        return DecorationGroup.from(n)
    }
    forChild(e, t) {
        if (t.isLeaf) return DecorationSet.empty;
        let n = [];
        for (let o = 0; o < this.members.length; o++) {
            let i = this.members[o].forChild(e, t);
            i != Tn && (i instanceof DecorationGroup ? n = n.concat(i.members) : n.push(i))
        }
        return DecorationGroup.from(n)
    }
    eq(e) {
        if (!(e instanceof DecorationGroup) || e.members.length != this.members.length) return false;
        for (let t = 0; t < this.members.length; t++)
            if (!this.members[t].eq(e.members[t])) return false;
        return true
    }
    locals(e) {
        let t, n = true;
        for (let o = 0; o < this.members.length; o++) {
            let i = this.members[o].localsInner(e);
            if (i.length)
                if (t) {
                    if (n) {
                        t = t.slice();
                        n = false
                    }
                    for (let e = 0; e < i.length; e++) t.push(i[e])
                } else t = i
        }
        return t ? In(n ? t : t.sort(Bn)) : Mn
    }
    static from(e) {
        switch (e.length) {
            case 0:
                return Tn;
            case 1:
                return e[0];
            default:
                return new DecorationGroup(e.every((e => e instanceof DecorationSet)) ? e : e.reduce(((e, t) => e.concat(t instanceof DecorationSet ? t : t.members)), []))
        }
    }
    forEachSet(e) {
        for (let t = 0; t < this.members.length; t++) this.members[t].forEachSet(e)
    }
}

function kn(e, t, n, o, i, s, r) {
    let l = e.slice();
    for (let e = 0, t = s; e < n.maps.length; e++) {
        let o = 0;
        n.maps[e].forEach(((e, n, i, s) => {
            let r = s - i - (n - e);
            for (let i = 0; i < l.length; i += 3) {
                let s = l[i + 1];
                if (s < 0 || e > s + t - o) continue;
                let a = l[i] + t - o;
                if (n >= a) l[i + 1] = e <= a ? -2 : -1;
                else if (e >= t && r) {
                    l[i] += r;
                    l[i + 1] += r
                }
            }
            o += r
        }));
        t = n.maps[e].map(t, -1)
    }
    let a = false;
    for (let t = 0; t < l.length; t += 3)
        if (l[t + 1] < 0) {
            if (l[t + 1] == -2) {
                a = true;
                l[t + 1] = -1;
                continue
            }
            let d = n.map(e[t] + s),
                c = d - i;
            if (c < 0 || c >= o.content.size) {
                a = true;
                continue
            }
            let h = n.map(e[t + 1] + s, -1),
                f = h - i;
            let {
                index: u,
                offset: p
            } = o.content.findIndex(c);
            let m = o.maybeChild(u);
            if (m && p == c && p + m.nodeSize == f) {
                let o = l[t + 2].mapInner(n, m, d + 1, e[t] + s + 1, r);
                if (o != Tn) {
                    l[t] = c;
                    l[t + 1] = f;
                    l[t + 2] = o
                } else {
                    l[t + 1] = -2;
                    a = true
                }
            } else a = true
        } if (a) {
        let a = En(l, e, t, n, i, s, r);
        let d = Rn(a, o, 0, r);
        t = d.local;
        for (let e = 0; e < l.length; e += 3)
            if (l[e + 1] < 0) {
                l.splice(e, 3);
                e -= 3
            } for (let e = 0, t = 0; e < d.children.length; e += 3) {
            let n = d.children[e];
            while (t < l.length && l[t] < n) t += 3;
            l.splice(t, 0, d.children[e], d.children[e + 1], d.children[e + 2])
        }
    }
    return new DecorationSet(t.sort(Bn), l)
}

function Vn(e, t) {
    if (!t || !e.length) return e;
    let n = [];
    for (let o = 0; o < e.length; o++) {
        let i = e[o];
        n.push(new Decoration(i.from + t, i.to + t, i.type))
    }
    return n
}

function En(e, t, n, o, i, s, r) {
    function l(e, t) {
        for (let s = 0; s < e.local.length; s++) {
            let l = e.local[s].map(o, i, t);
            l ? n.push(l) : r.onRemove && r.onRemove(e.local[s].spec)
        }
        for (let n = 0; n < e.children.length; n += 3) l(e.children[n + 2], e.children[n] + t + 1)
    }
    for (let n = 0; n < e.length; n += 3) e[n + 1] == -1 && l(e[n + 2], t[n] + s + 1);
    return n
}

function Pn(e, t, n) {
    if (t.isLeaf) return null;
    let o = n + t.nodeSize,
        i = null;
    for (let t, s = 0; s < e.length; s++)
        if ((t = e[s]) && t.from > n && t.to < o) {
            (i || (i = [])).push(t);
            e[s] = null
        } return i
}

function An(e) {
    let t = [];
    for (let n = 0; n < e.length; n++) e[n] != null && t.push(e[n]);
    return t
}

function Rn(e, t, n, o) {
    let i = [],
        s = false;
    t.forEach(((t, r) => {
        let l = Pn(e, t, r + n);
        if (l) {
            s = true;
            let e = Rn(l, t, n + r + 1, o);
            e != Tn && i.push(r, r + t.nodeSize, e)
        }
    }));
    let r = Vn(s ? An(e) : e, -n).sort(Bn);
    for (let e = 0; e < r.length; e++)
        if (!r[e].type.valid(t, r[e])) {
            o.onRemove && o.onRemove(r[e].spec);
            r.splice(e--, 1)
        } return r.length || i.length ? new DecorationSet(r, i) : Tn
}

function Bn(e, t) {
    return e.from - t.from || e.to - t.to
}

function In(e) {
    let t = e;
    for (let n = 0; n < t.length - 1; n++) {
        let o = t[n];
        if (o.from != o.to)
            for (let i = n + 1; i < t.length; i++) {
                let s = t[i];
                if (s.from != o.from) {
                    if (s.from < o.to) {
                        t == e && (t = e.slice());
                        t[n] = o.copy(o.from, s.from);
                        zn(t, i, o.copy(s.from, o.to))
                    }
                    break
                }
                if (s.to != o.to) {
                    t == e && (t = e.slice());
                    t[i] = s.copy(s.from, o.to);
                    zn(t, i + 1, s.copy(o.to, s.to))
                }
            }
    }
    return t
}

function zn(e, t, n) {
    while (t < e.length && Bn(n, e[t]) > 0) t++;
    e.splice(t, 0, n)
}

function Ln(e) {
    let t = [];
    e.someProp("decorations", (n => {
        let o = n(e.state);
        o && o != Tn && t.push(o)
    }));
    e.cursorWrapper && t.push(DecorationSet.create(e.state.doc, [e.cursorWrapper.deco]));
    return DecorationGroup.from(t)
}
const Fn = {
    childList: true,
    characterData: true,
    characterDataOldValue: true,
    attributes: true,
    attributeOldValue: true,
    subtree: true
};
const $n = A && R <= 11;
class SelectionState {
    constructor() {
        this.anchorNode = null;
        this.anchorOffset = 0;
        this.focusNode = null;
        this.focusOffset = 0
    }
    set(e) {
        this.anchorNode = e.anchorNode;
        this.anchorOffset = e.anchorOffset;
        this.focusNode = e.focusNode;
        this.focusOffset = e.focusOffset
    }
    clear() {
        this.anchorNode = this.focusNode = null
    }
    eq(e) {
        return e.anchorNode == this.anchorNode && e.anchorOffset == this.anchorOffset && e.focusNode == this.focusNode && e.focusOffset == this.focusOffset
    }
}
class DOMObserver {
    constructor(e, t) {
        this.view = e;
        this.handleDOMChange = t;
        this.queue = [];
        this.flushingSoon = -1;
        this.observer = null;
        this.currentSelection = new SelectionState;
        this.onCharData = null;
        this.suppressingSelectionUpdates = false;
        this.lastChangedTextNode = null;
        this.observer = window.MutationObserver && new window.MutationObserver((e => {
            for (let t = 0; t < e.length; t++) this.queue.push(e[t]);
            A && R <= 11 && e.some((e => e.type == "childList" && e.removedNodes.length || e.type == "characterData" && e.oldValue.length > e.target.nodeValue.length)) ? this.flushSoon() : this.flush()
        }));
        $n && (this.onCharData = e => {
            this.queue.push({
                target: e.target,
                type: "characterData",
                oldValue: e.prevValue
            });
            this.flushSoon()
        });
        this.onSelectionChange = this.onSelectionChange.bind(this)
    }
    flushSoon() {
        this.flushingSoon < 0 && (this.flushingSoon = window.setTimeout((() => {
            this.flushingSoon = -1;
            this.flush()
        }), 20))
    }
    forceFlush() {
        if (this.flushingSoon > -1) {
            window.clearTimeout(this.flushingSoon);
            this.flushingSoon = -1;
            this.flush()
        }
    }
    start() {
        if (this.observer) {
            this.observer.takeRecords();
            this.observer.observe(this.view.dom, Fn)
        }
        this.onCharData && this.view.dom.addEventListener("DOMCharacterDataModified", this.onCharData);
        this.connectSelection()
    }
    stop() {
        if (this.observer) {
            let e = this.observer.takeRecords();
            if (e.length) {
                for (let t = 0; t < e.length; t++) this.queue.push(e[t]);
                window.setTimeout((() => this.flush()), 20)
            }
            this.observer.disconnect()
        }
        this.onCharData && this.view.dom.removeEventListener("DOMCharacterDataModified", this.onCharData);
        this.disconnectSelection()
    }
    connectSelection() {
        this.view.dom.ownerDocument.addEventListener("selectionchange", this.onSelectionChange)
    }
    disconnectSelection() {
        this.view.dom.ownerDocument.removeEventListener("selectionchange", this.onSelectionChange)
    }
    suppressSelectionUpdates() {
        this.suppressingSelectionUpdates = true;
        setTimeout((() => this.suppressingSelectionUpdates = false), 50)
    }
    onSelectionChange() {
        if (nt(this.view)) {
            if (this.suppressingSelectionUpdates) return Ge(this.view);
            if (A && R <= 11 && !this.view.state.selection.empty) {
                let e = this.view.domSelectionRange();
                if (e.focusNode && m(e.focusNode, e.focusOffset, e.anchorNode, e.anchorOffset)) return this.flushSoon()
            }
            this.flush()
        }
    }
    setCurSelection() {
        this.currentSelection.set(this.view.domSelectionRange())
    }
    ignoreSelectionChange(e) {
        if (!e.focusNode) return true;
        let t, n = new Set;
        for (let t = e.focusNode; t; t = h(t)) n.add(t);
        for (let o = e.anchorNode; o; o = h(o))
            if (n.has(o)) {
                t = o;
                break
            } let o = t && this.view.docView.nearestDesc(t);
        if (o && o.ignoreMutation({
                type: "selection",
                target: t.nodeType == 3 ? t.parentNode : t
            })) {
            this.setCurSelection();
            return true
        }
    }
    pendingRecords() {
        if (this.observer)
            for (let e of this.observer.takeRecords()) this.queue.push(e);
        return this.queue
    }
    flush() {
        let {
            view: e
        } = this;
        if (!e.docView || this.flushingSoon > -1) return;
        let t = this.pendingRecords();
        t.length && (this.queue = []);
        let o = e.domSelectionRange();
        let i = !this.suppressingSelectionUpdates && !this.currentSelection.eq(o) && nt(e) && !this.ignoreSelectionChange(o);
        let s = -1,
            r = -1,
            l = false,
            a = [];
        if (e.editable)
            for (let e = 0; e < t.length; e++) {
                let n = this.registerMutation(t[e], a);
                if (n) {
                    s = s < 0 ? n.from : Math.min(n.from, s);
                    r = r < 0 ? n.to : Math.max(n.to, r);
                    n.typeOver && (l = true)
                }
            }
        if (B && a.length) {
            let t = a.filter((e => e.nodeName == "BR"));
            if (t.length == 2) {
                let [e, n] = t;
                e.parentNode && e.parentNode.parentNode == n.parentNode ? n.remove() : e.remove()
            } else {
                let {
                    focusNode: n
                } = this.currentSelection;
                for (let o of t) {
                    let t = o.parentNode;
                    !t || t.nodeName != "LI" || n && Gn(e, n) == t || o.remove()
                }
            }
        }
        let d = null;
        if (s < 0 && i && e.input.lastFocus > Date.now() - 200 && Math.max(e.input.lastTouch, e.input.lastClick.time) < Date.now() - 300 && S(o) && (d = He(e)) && d.eq(n.near(e.state.doc.resolve(0), 1))) {
            e.input.lastFocus = 0;
            Ge(e);
            this.currentSelection.set(o);
            e.scrollToSelection()
        } else if (s > -1 || i) {
            if (s > -1) {
                e.docView.markDirty(s, r);
                Wn(e)
            }
            this.handleDOMChange(s, r, l, a);
            e.docView && e.docView.dirty ? e.updateState(e.state) : this.currentSelection.eq(o) || Ge(e);
            this.currentSelection.set(o)
        }
    }
    registerMutation(e, t) {
        if (t.indexOf(e.target) > -1) return null;
        let n = this.view.docView.nearestDesc(e.target);
        if (e.type == "attributes" && (n == this.view.docView || e.attributeName == "contenteditable" || e.attributeName == "style" && !e.oldValue && !e.target.getAttribute("style"))) return null;
        if (!n || n.ignoreMutation(e)) return null;
        if (e.type == "childList") {
            for (let n = 0; n < e.addedNodes.length; n++) {
                let o = e.addedNodes[n];
                t.push(o);
                o.nodeType == 3 && (this.lastChangedTextNode = o)
            }
            if (n.contentDOM && n.contentDOM != n.dom && !n.contentDOM.contains(e.target)) return {
                from: n.posBefore,
                to: n.posAfter
            };
            let o = e.previousSibling,
                i = e.nextSibling;
            if (A && R <= 11 && e.addedNodes.length)
                for (let t = 0; t < e.addedNodes.length; t++) {
                    let {
                        previousSibling: n,
                        nextSibling: s
                    } = e.addedNodes[t];
                    (!n || Array.prototype.indexOf.call(e.addedNodes, n) < 0) && (o = n);
                    (!s || Array.prototype.indexOf.call(e.addedNodes, s) < 0) && (i = s)
                }
            let s = o && o.parentNode == e.target ? c(o) + 1 : 0;
            let r = n.localPosFromDOM(e.target, s, -1);
            let l = i && i.parentNode == e.target ? c(i) : e.target.childNodes.length;
            let a = n.localPosFromDOM(e.target, l, 1);
            return {
                from: r,
                to: a
            }
        }
        if (e.type == "attributes") return {
            from: n.posAtStart - n.border,
            to: n.posAtEnd + n.border
        };
        this.lastChangedTextNode = e.target;
        return {
            from: n.posAtStart,
            to: n.posAtEnd,
            typeOver: e.target.nodeValue == e.oldValue
        }
    }
}
let qn = new WeakMap;
let Kn = false;

function Wn(e) {
    if (!qn.has(e)) {
        qn.set(e, null);
        if (["normal", "nowrap", "pre-line"].indexOf(getComputedStyle(e.dom).whiteSpace) !== -1) {
            e.requiresGeckoHackNode = B;
            if (Kn) return;
            console.warn("ProseMirror expects the CSS white-space property to be set, preferably to 'pre-wrap'. It is recommended to load style/prosemirror.css from the prosemirror-view package.");
            Kn = true
        }
    }
}

function Hn(e, t) {
    let n = t.startContainer,
        o = t.startOffset;
    let i = t.endContainer,
        s = t.endOffset;
    let r = e.domAtPos(e.state.selection.anchor);
    m(r.node, r.offset, i, s) && ([n, o, i, s] = [i, s, n, o]);
    return {
        anchorNode: n,
        anchorOffset: o,
        focusNode: i,
        focusOffset: s
    }
}

function _n(e, t) {
    if (t.getComposedRanges) {
        let n = t.getComposedRanges(e.root)[0];
        if (n) return Hn(e, n)
    }
    let n;

    function o(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        n = e.getTargetRanges()[0]
    }
    e.dom.addEventListener("beforeinput", o, true);
    document.execCommand("indent");
    e.dom.removeEventListener("beforeinput", o, true);
    return n ? Hn(e, n) : null
}

function Gn(e, t) {
    for (let n = t.parentNode; n && n != e.dom; n = n.parentNode) {
        let t = e.docView.nearestDesc(n, true);
        if (t && t.node.isBlock) return n
    }
    return null
}

function Un(e, t, n) {
    let {
        node: o,
        fromOffset: i,
        toOffset: s,
        from: r,
        to: l
    } = e.docView.parseRange(t, n);
    let d = e.domSelectionRange();
    let c;
    let h = d.anchorNode;
    if (h && e.dom.contains(h.nodeType == 1 ? h : h.parentNode)) {
        c = [{
            node: h,
            offset: d.anchorOffset
        }];
        S(d) || c.push({
            node: d.focusNode,
            offset: d.focusOffset
        })
    }
    if (z && e.input.lastKeyCode === 8)
        for (let e = s; e > i; e--) {
            let t = o.childNodes[e - 1],
                n = t.pmViewDesc;
            if (t.nodeName == "BR" && !n) {
                s = e;
                break
            }
            if (!n || n.size) break
        }
    let f = e.state.doc;
    let u = e.someProp("domParser") || a.fromSchema(e.state.schema);
    let p = f.resolve(r);
    let m = null,
        g = u.parse(o, {
            topNode: p.parent,
            topMatch: p.parent.contentMatchAt(p.index()),
            topOpen: true,
            from: i,
            to: s,
            preserveWhitespace: p.parent.type.whitespace != "pre" || "full",
            findPositions: c,
            ruleFromNode: jn,
            context: p
        });
    if (c && c[0].pos != null) {
        let e = c[0].pos,
            t = c[1] && c[1].pos;
        t == null && (t = e);
        m = {
            anchor: e + r,
            head: t + r
        }
    }
    return {
        doc: g,
        sel: m,
        from: r,
        to: l
    }
}

function jn(e) {
    let t = e.pmViewDesc;
    if (t) return t.parseRule();
    if (e.nodeName == "BR" && e.parentNode) {
        if (F && /^(ul|ol)$/i.test(e.parentNode.nodeName)) {
            let e = document.createElement("div");
            e.appendChild(document.createElement("li"));
            return {
                skip: e
            }
        }
        if (e.parentNode.lastChild == e || F && /^(tr|table)$/i.test(e.parentNode.nodeName)) return {
            ignore: true
        }
    } else if (e.nodeName == "IMG" && e.getAttribute("mark-placeholder")) return {
        ignore: true
    };
    return null
}
const Xn = /^(a|abbr|acronym|b|bd[io]|big|br|button|cite|code|data(list)?|del|dfn|em|i|ins|kbd|label|map|mark|meter|output|q|ruby|s|samp|small|span|strong|su[bp]|time|u|tt|var)$/i;

function Yn(t, o, i, s, r) {
    let l = t.input.compositionPendingChanges || (t.composing ? t.input.compositionID : 0);
    t.input.compositionPendingChanges = 0;
    if (o < 0) {
        let e = t.input.lastSelectionTime > Date.now() - 50 ? t.input.lastSelectionOrigin : null;
        let n = He(t, e);
        if (n && !t.state.selection.eq(n)) {
            if (z && W && t.input.lastKeyCode === 13 && Date.now() - 100 < t.input.lastKeyCodeTime && t.someProp("handleKeyDown", (e => e(t, O(13, "Enter"))))) return;
            let o = t.state.tr.setSelection(n);
            e == "pointer" ? o.setMeta("pointer", true) : e == "key" && o.scrollIntoView();
            l && o.setMeta("composition", l);
            t.dispatch(o)
        }
        return
    }
    let a = t.state.doc.resolve(o);
    let d = a.sharedDepth(i);
    o = a.before(d + 1);
    i = t.state.doc.resolve(i).after(d + 1);
    let c = t.state.selection;
    let h = Un(t, o, i);
    let f = t.state.doc,
        u = f.slice(h.from, h.to);
    let p, m;
    if (t.input.lastKeyCode === 8 && Date.now() - 100 < t.input.lastKeyCodeTime) {
        p = t.state.selection.to;
        m = "end"
    } else {
        p = t.state.selection.from;
        m = "start"
    }
    t.input.lastKeyCode = null;
    let g = to(u.content, h.doc.content, h.from, p, m);
    g && t.input.domChangeCount++;
    if (($ && t.input.lastIOSEnter > Date.now() - 225 || W) && r.some((e => e.nodeType == 1 && !Xn.test(e.nodeName))) && (!g || g.endA >= g.endB) && t.someProp("handleKeyDown", (e => e(t, O(13, "Enter"))))) {
        t.input.lastIOSEnter = 0;
        return
    }
    if (!g) {
        if (!(s && c instanceof e && !c.empty && c.$head.sameParent(c.$anchor)) || t.composing || h.sel && h.sel.anchor != h.sel.head) {
            if (h.sel) {
                let e = Jn(t, t.state.doc, h.sel);
                if (e && !e.eq(t.state.selection)) {
                    let n = t.state.tr.setSelection(e);
                    l && n.setMeta("composition", l);
                    t.dispatch(n)
                }
            }
            return
        }
        g = {
            start: c.from,
            endA: c.to,
            endB: c.to
        }
    }
    if (t.state.selection.from < t.state.selection.to && g.start == g.endB && t.state.selection instanceof e)
        if (g.start > t.state.selection.from && g.start <= t.state.selection.from + 2 && t.state.selection.from >= h.from) g.start = t.state.selection.from;
        else if (g.endA < t.state.selection.to && g.endA >= t.state.selection.to - 2 && t.state.selection.to <= h.to) {
        g.endB += t.state.selection.to - g.endA;
        g.endA = t.state.selection.to
    }
    if (A && R <= 11 && g.endB == g.start + 1 && g.endA == g.start && g.start > h.from && h.doc.textBetween(g.start - h.from - 1, g.start - h.from + 1) == "  ") {
        g.start--;
        g.endA--;
        g.endB--
    }
    let y = h.doc.resolveNoCache(g.start - h.from);
    let w = h.doc.resolveNoCache(g.endB - h.from);
    let b = f.resolve(g.start);
    let D = y.sameParent(w) && y.parent.inlineContent && b.end() >= g.endA;
    let v;
    if (($ && t.input.lastIOSEnter > Date.now() - 225 && (!D || r.some((e => e.nodeName == "DIV" || e.nodeName == "P"))) || !D && y.pos < h.doc.content.size && (!y.sameParent(w) || !y.parent.inlineContent) && !/\S/.test(h.doc.textBetween(y.pos, w.pos, "", "")) && (v = n.findFrom(h.doc.resolve(y.pos + 1), 1, true)) && v.head > y.pos) && t.someProp("handleKeyDown", (e => e(t, O(13, "Enter"))))) {
        t.input.lastIOSEnter = 0;
        return
    }
    if (t.state.selection.anchor > g.start && Zn(f, g.start, g.endA, y, w) && t.someProp("handleKeyDown", (e => e(t, O(8, "Backspace"))))) {
        W && z && t.domObserver.suppressSelectionUpdates();
        return
    }
    z && g.endB == g.start && (t.input.lastChromeDelete = Date.now());
    if (W && !D && y.start() != w.start() && w.parentOffset == 0 && y.depth == w.depth && h.sel && h.sel.anchor == h.sel.head && h.sel.head == g.endA) {
        g.endB -= 2;
        w = h.doc.resolveNoCache(g.endB - h.from);
        setTimeout((() => {
            t.someProp("handleKeyDown", (function(e) {
                return e(t, O(13, "Enter"))
            }))
        }), 20)
    }
    let N = g.start,
        S = g.endA;
    let C, M, x;
    if (D)
        if (y.pos == w.pos) {
            if (A && R <= 11 && y.parentOffset == 0) {
                t.domObserver.suppressSelectionUpdates();
                setTimeout((() => Ge(t)), 20)
            }
            C = t.state.tr.delete(N, S);
            M = f.resolve(g.start).marksAcross(f.resolve(g.endA))
        } else if (g.endA == g.endB && (x = Qn(y.parent.content.cut(y.parentOffset, w.parentOffset), b.parent.content.cut(b.parentOffset, g.endA - b.start())))) {
        C = t.state.tr;
        x.type == "add" ? C.addMark(N, S, x.mark) : C.removeMark(N, S, x.mark)
    } else if (y.parent.child(y.index()).isText && y.index() == w.index() - (w.textOffset ? 0 : 1)) {
        let e = y.parent.textBetween(y.parentOffset, w.parentOffset);
        if (t.someProp("handleTextInput", (n => n(t, N, S, e)))) return;
        C = t.state.tr.insertText(e, N, S)
    }
    C || (C = t.state.tr.replace(N, S, h.doc.slice(g.start - h.from, g.endB - h.from)));
    if (h.sel) {
        let e = Jn(t, C.doc, h.sel);
        e && !(z && t.composing && e.empty && (g.start != g.endB || t.input.lastChromeDelete < Date.now() - 100) && (e.head == N || e.head == C.mapping.map(S) - 1) || A && e.empty && e.head == N) && C.setSelection(e)
    }
    M && C.ensureMarks(M);
    l && C.setMeta("composition", l);
    t.dispatch(C.scrollIntoView())
}

function Jn(e, t, n) {
    return Math.max(n.anchor, n.head) > t.content.size ? null : tt(e, t.resolve(n.anchor), t.resolve(n.head))
}

function Qn(e, t) {
    let n = e.firstChild.marks,
        o = t.firstChild.marks;
    let i, r, l, a = n,
        d = o;
    for (let e = 0; e < o.length; e++) a = o[e].removeFromSet(a);
    for (let e = 0; e < n.length; e++) d = n[e].removeFromSet(d);
    if (a.length == 1 && d.length == 0) {
        r = a[0];
        i = "add";
        l = e => e.mark(r.addToSet(e.marks))
    } else {
        if (a.length != 0 || d.length != 1) return null;
        r = d[0];
        i = "remove";
        l = e => e.mark(r.removeFromSet(e.marks))
    }
    let c = [];
    for (let e = 0; e < t.childCount; e++) c.push(l(t.child(e)));
    if (s.from(c).eq(e)) return {
        mark: r,
        type: i
    }
}

function Zn(e, t, n, o, i) {
    if (n - t <= i.pos - o.pos || eo(o, true, false) < i.pos) return false;
    let s = e.resolve(t);
    if (!o.parent.isTextblock) {
        let e = s.nodeAfter;
        return e != null && n == t + e.nodeSize
    }
    if (s.parentOffset < s.parent.content.size || !s.parent.isTextblock) return false;
    let r = e.resolve(eo(s, true, true));
    return !(!r.parent.isTextblock || r.pos > n || eo(r, true, false) < n) && o.parent.content.cut(o.parentOffset).eq(r.parent.content)
}

function eo(e, t, n) {
    let o = e.depth,
        i = t ? e.end() : e.pos;
    while (o > 0 && (t || e.indexAfter(o) == e.node(o).childCount)) {
        o--;
        i++;
        t = false
    }
    if (n) {
        let t = e.node(o).maybeChild(e.indexAfter(o));
        while (t && !t.isLeaf) {
            t = t.firstChild;
            i++
        }
    }
    return i
}

function to(e, t, n, o, i) {
    let s = e.findDiffStart(t, n);
    if (s == null) return null;
    let {
        a: r,
        b: l
    } = e.findDiffEnd(t, n + e.size, n + t.size);
    if (i == "end") {
        let e = Math.max(0, s - Math.min(r, l));
        o -= r + e - s
    }
    if (r < s && e.size < t.size) {
        let e = o <= s && o >= r ? s - o : 0;
        s -= e;
        s && s < t.size && no(t.textBetween(s - 1, s + 1)) && (s += e ? 1 : -1);
        l = s + (l - r);
        r = s
    } else if (l < s) {
        let t = o <= s && o >= l ? s - o : 0;
        s -= t;
        s && s < e.size && no(e.textBetween(s - 1, s + 1)) && (s += t ? 1 : -1);
        r = s + (r - l);
        l = s
    }
    return {
        start: s,
        endA: r,
        endB: l
    }
}

function no(e) {
    if (e.length != 2) return false;
    let t = e.charCodeAt(0),
        n = e.charCodeAt(1);
    return t >= 56320 && t <= 57343 && n >= 55296 && n <= 56319
}
const oo = Ct;
const io = gn;
class EditorView {
    constructor(e, t) {
        this._root = null;
        this.focused = false;
        this.trackWrites = null;
        this.mounted = false;
        this.markCursor = null;
        this.cursorWrapper = null;
        this.lastSelectedViewDesc = void 0;
        this.input = new InputState;
        this.prevDirectPlugins = [];
        this.pluginViews = [];
        this.requiresGeckoHackNode = false;
        this.dragging = null;
        this._props = t;
        this.state = t.state;
        this.directPlugins = t.plugins || [];
        this.directPlugins.forEach(fo);
        this.dispatch = this.dispatch.bind(this);
        this.dom = e && e.mount || document.createElement("div");
        e && (e.appendChild ? e.appendChild(this.dom) : typeof e == "function" ? e(this.dom) : e.mount && (this.mounted = true));
        this.editable = lo(this);
        ro(this);
        this.nodeViews = co(this);
        this.docView = Te(this.state.doc, so(this), Ln(this), this.dom, this);
        this.domObserver = new DOMObserver(this, ((e, t, n, o) => Yn(this, e, t, n, o)));
        this.domObserver.start();
        Ht(this);
        this.updatePluginViews()
    }
    get composing() {
        return this.input.composing
    }
    get props() {
        if (this._props.state != this.state) {
            let e = this._props;
            this._props = {};
            for (let t in e) this._props[t] = e[t];
            this._props.state = this.state
        }
        return this._props
    }
    update(e) {
        e.handleDOMEvents != this._props.handleDOMEvents && Ut(this);
        let t = this._props;
        this._props = e;
        if (e.plugins) {
            e.plugins.forEach(fo);
            this.directPlugins = e.plugins
        }
        this.updateStateInner(e.state, t)
    }
    setProps(e) {
        let t = {};
        for (let e in this._props) t[e] = this._props[e];
        t.state = this.state;
        for (let n in e) t[n] = e[n];
        this.update(t)
    }
    updateState(e) {
        this.updateStateInner(e, this._props)
    }
    updateStateInner(e, t) {
        var n;
        let o = this.state,
            i = false,
            s = false;
        if (e.storedMarks && this.composing) {
            un(this);
            s = true
        }
        this.state = e;
        let r = o.plugins != e.plugins || this._props.plugins != t.plugins;
        if (r || this._props.plugins != t.plugins || this._props.nodeViews != t.nodeViews) {
            let e = co(this);
            if (ho(e, this.nodeViews)) {
                this.nodeViews = e;
                i = true
            }
        }(r || t.handleDOMEvents != this._props.handleDOMEvents) && Ut(this);
        this.editable = lo(this);
        ro(this);
        let l = Ln(this),
            a = so(this);
        let d = o.plugins == e.plugins || o.doc.eq(e.doc) ? e.scrollToSelection > o.scrollToSelection ? "to selection" : "preserve" : "reset";
        let c = i || !this.docView.matchesNode(e.doc, a, l);
        !c && e.selection.eq(o.selection) || (s = true);
        let h = d == "preserve" && s && this.dom.style.overflowAnchor == null && Y(this);
        if (s) {
            this.domObserver.stop();
            let t = c && (A || z) && !this.composing && !o.selection.empty && !e.selection.empty && ao(o.selection, e.selection);
            if (c) {
                let n = z ? this.trackWrites = this.domSelectionRange().focusNode : null;
                this.composing && (this.input.compositionNode = pn(this));
                if (i || !this.docView.update(e.doc, a, l, this)) {
                    this.docView.updateOuterDeco(a);
                    this.docView.destroy();
                    this.docView = Te(e.doc, a, l, this.dom, this)
                }
                n && !this.trackWrites && (t = true)
            }
            if (t || !(this.input.mouseDown && this.domObserver.currentSelection.eq(this.domSelectionRange()) && it(this))) Ge(this, t);
            else {
                Ze(this, e.selection);
                this.domObserver.setCurSelection()
            }
            this.domObserver.start()
        }
        this.updatePluginViews(o);
        ((n = this.dragging) === null || n === void 0 ? void 0 : n.node) && !o.doc.eq(e.doc) && this.updateDraggedNode(this.dragging, o);
        d == "reset" ? this.dom.scrollTop = 0 : d == "to selection" ? this.scrollToSelection() : h && Q(h)
    }
    scrollToSelection() {
        let e = this.domSelectionRange().focusNode;
        if (e && this.dom.contains(e.nodeType == 1 ? e : e.parentNode))
            if (this.someProp("handleScrollToSelection", (e => e(this))));
            else if (this.state.selection instanceof t) {
            let t = this.docView.domAfterPos(this.state.selection.from);
            t.nodeType == 1 && X(this, t.getBoundingClientRect(), e)
        } else X(this, this.coordsAtPos(this.state.selection.head, 1), e);
        else;
    }
    destroyPluginViews() {
        let e;
        while (e = this.pluginViews.pop()) e.destroy && e.destroy()
    }
    updatePluginViews(e) {
        if (e && e.plugins == this.state.plugins && this.directPlugins == this.prevDirectPlugins)
            for (let t = 0; t < this.pluginViews.length; t++) {
                let n = this.pluginViews[t];
                n.update && n.update(this, e)
            } else {
                this.prevDirectPlugins = this.directPlugins;
                this.destroyPluginViews();
                for (let e = 0; e < this.directPlugins.length; e++) {
                    let t = this.directPlugins[e];
                    t.spec.view && this.pluginViews.push(t.spec.view(this))
                }
                for (let e = 0; e < this.state.plugins.length; e++) {
                    let t = this.state.plugins[e];
                    t.spec.view && this.pluginViews.push(t.spec.view(this))
                }
            }
    }
    updateDraggedNode(e, n) {
        let o = e.node,
            i = -1;
        if (this.state.doc.nodeAt(o.from) == o.node) i = o.from;
        else {
            let e = o.from + (this.state.doc.content.size - n.doc.content.size);
            let t = e > 0 && this.state.doc.nodeAt(e);
            t == o.node && (i = e)
        }
        this.dragging = new Dragging(e.slice, e.move, i < 0 ? void 0 : t.create(this.state.doc, i))
    }
    someProp(e, t) {
        let n, o = this._props && this._props[e];
        if (o != null && (n = t ? t(o) : o)) return n;
        for (let o = 0; o < this.directPlugins.length; o++) {
            let i = this.directPlugins[o].props[e];
            if (i != null && (n = t ? t(i) : i)) return n
        }
        let i = this.state.plugins;
        if (i)
            for (let o = 0; o < i.length; o++) {
                let s = i[o].props[e];
                if (s != null && (n = t ? t(s) : s)) return n
            }
    }
    hasFocus() {
        if (A) {
            let e = this.root.activeElement;
            if (e == this.dom) return true;
            if (!e || !this.dom.contains(e)) return false;
            while (e && this.dom != e && this.dom.contains(e)) {
                if (e.contentEditable == "false") return false;
                e = e.parentElement
            }
            return true
        }
        return this.root.activeElement == this.dom
    }
    focus() {
        this.domObserver.stop();
        this.editable && te(this.dom);
        Ge(this);
        this.domObserver.start()
    }
    get root() {
        let e = this._root;
        if (e == null)
            for (let e = this.dom.parentNode; e; e = e.parentNode)
                if (e.nodeType == 9 || e.nodeType == 11 && e.host) {
                    e.getSelection || (Object.getPrototypeOf(e).getSelection = () => e.ownerDocument.getSelection());
                    return this._root = e
                } return e || document
    }
    updateRoot() {
        this._root = null
    }
    posAtCoords(e) {
        return de(this, e)
    }
    coordsAtPos(e, t = 1) {
        return ue(this, e, t)
    }
    domAtPos(e, t = 0) {
        return this.docView.domFromPos(e, t)
    }
    nodeDOM(e) {
        let t = this.docView.descAt(e);
        return t ? t.nodeDOM : null
    }
    posAtDOM(e, t, n = -1) {
        let o = this.docView.posFromDOM(e, t, n);
        if (o == null) throw new RangeError("DOM position not inside the editor");
        return o
    }
    endOfTextblock(e, t) {
        return Se(this, t || this.state, e)
    }
    pasteHTML(e, t) {
        return vn(this, "", e, false, t || new ClipboardEvent("paste"))
    }
    pasteText(e, t) {
        return vn(this, e, null, true, t || new ClipboardEvent("paste"))
    }
    serializeForClipboard(e) {
        return Ot(this, e)
    }
    destroy() {
        if (this.docView) {
            Gt(this);
            this.destroyPluginViews();
            if (this.mounted) {
                this.docView.update(this.state.doc, [], Ln(this), this);
                this.dom.textContent = ""
            } else this.dom.parentNode && this.dom.parentNode.removeChild(this.dom);
            this.docView.destroy();
            this.docView = null;
            p()
        }
    }
    get isDestroyed() {
        return this.docView == null
    }
    dispatchEvent(e) {
        return Yt(this, e)
    }
    dispatch(e) {
        let t = this._props.dispatchTransaction;
        t ? t.call(this, e) : this.updateState(this.state.apply(e))
    }
    domSelectionRange() {
        let e = this.domSelection();
        return e ? F && this.root.nodeType === 11 && C(this.dom.ownerDocument) == this.dom && _n(this, e) || e : {
            focusNode: null,
            focusOffset: 0,
            anchorNode: null,
            anchorOffset: 0
        }
    }
    domSelection() {
        return this.root.getSelection()
    }
}

function so(e) {
    let t = Object.create(null);
    t.class = "ProseMirror";
    t.contenteditable = String(e.editable);
    e.someProp("attributes", (n => {
        typeof n == "function" && (n = n(e.state));
        if (n)
            for (let e in n) e == "class" ? t.class += " " + n[e] : e == "style" ? t.style = (t.style ? t.style + ";" : "") + n[e] : t[e] || e == "contenteditable" || e == "nodeName" || (t[e] = String(n[e]))
    }));
    t.translate || (t.translate = "no");
    return [Decoration.node(0, e.state.doc.content.size, t)]
}

function ro(e) {
    if (e.markCursor) {
        let t = document.createElement("img");
        t.className = "ProseMirror-separator";
        t.setAttribute("mark-placeholder", "true");
        t.setAttribute("alt", "");
        e.cursorWrapper = {
            dom: t,
            deco: Decoration.widget(e.state.selection.from, t, {
                raw: true,
                marks: e.markCursor
            })
        }
    } else e.cursorWrapper = null
}

function lo(e) {
    return !e.someProp("editable", (t => t(e.state) === false))
}

function ao(e, t) {
    let n = Math.min(e.$anchor.sharedDepth(e.head), t.$anchor.sharedDepth(t.head));
    return e.$anchor.start(n) != t.$anchor.start(n)
}

function co(e) {
    let t = Object.create(null);

    function n(e) {
        for (let n in e) Object.prototype.hasOwnProperty.call(t, n) || (t[n] = e[n])
    }
    e.someProp("nodeViews", n);
    e.someProp("markViews", n);
    return t
}

function ho(e, t) {
    let n = 0,
        o = 0;
    for (let o in e) {
        if (e[o] != t[o]) return true;
        n++
    }
    for (let e in t) o++;
    return n != o
}

function fo(e) {
    if (e.spec.state || e.spec.filterTransaction || e.spec.appendTransaction) throw new RangeError("Plugins passed directly to the view must not have a state component")
}
export {
    Decoration,
    DecorationSet,
    EditorView,
    io as __endComposition,
    oo as __parseFromClipboard
};