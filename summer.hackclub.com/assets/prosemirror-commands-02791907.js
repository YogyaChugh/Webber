// prosemirror-commands@1.7.1 downloaded from https://ga.jspm.io/npm:prosemirror-commands@1.7.1/dist/index.js

import {
    liftTarget as e,
    replaceStep as t,
    ReplaceStep as r,
    canJoin as n,
    joinPoint as o,
    canSplit as l,
    ReplaceAroundStep as s,
    findWrapping as i
} from "prosemirror-transform";
import {
    Slice as f,
    Fragment as c
} from "prosemirror-model";
import {
    NodeSelection as a,
    Selection as p,
    TextSelection as u,
    AllSelection as d,
    SelectionRange as h
} from "prosemirror-state";
const m = (e, t) => {
    if (e.selection.empty) return false;
    t && t(e.tr.deleteSelection().scrollIntoView());
    return true
};

function k(e, t) {
    let {
        $cursor: r
    } = e.selection;
    return !r || (t ? !t.endOfTextblock("backward", e) : r.parentOffset > 0) ? null : r
}
const g = (r, n, o) => {
    let l = k(r, o);
    if (!l) return false;
    let s = S(l);
    if (!s) {
        let t = l.blockRange(),
            o = t && e(t);
        if (o == null) return false;
        n && n(r.tr.lift(t, o).scrollIntoView());
        return true
    }
    let i = s.nodeBefore;
    if (G(r, s, n, -1)) return true;
    if (l.parent.content.size == 0 && (x(i, "end") || a.isSelectable(i)))
        for (let e = l.depth;; e--) {
            let o = t(r.doc, l.before(e), l.after(e), f.empty);
            if (o && o.slice.size < o.to - o.from) {
                if (n) {
                    let e = r.tr.step(o);
                    e.setSelection(x(i, "end") ? p.findFrom(e.doc.resolve(e.mapping.map(s.pos, -1)), -1) : a.create(e.doc, s.pos - i.nodeSize));
                    n(e.scrollIntoView())
                }
                return true
            }
            if (e == 1 || l.node(e - 1).childCount > 1) break
        }
    if (i.isAtom && s.depth == l.depth - 1) {
        n && n(r.tr.delete(s.pos - i.nodeSize, s.pos).scrollIntoView());
        return true
    }
    return false
};
const y = (e, t, r) => {
    let n = k(e, r);
    if (!n) return false;
    let o = S(n);
    return !!o && b(e, o, t)
};
const w = (e, t, r) => {
    let n = I(e, r);
    if (!n) return false;
    let o = T(n);
    return !!o && b(e, o, t)
};

function b(e, n, o) {
    let l = n.nodeBefore,
        s = l,
        i = n.pos - 1;
    for (; !s.isTextblock; i--) {
        if (s.type.spec.isolating) return false;
        let e = s.lastChild;
        if (!e) return false;
        s = e
    }
    let c = n.nodeAfter,
        a = c,
        p = n.pos + 1;
    for (; !a.isTextblock; p++) {
        if (a.type.spec.isolating) return false;
        let e = a.firstChild;
        if (!e) return false;
        a = e
    }
    let d = t(e.doc, i, p, f.empty);
    if (!d || d.from != i || d instanceof r && d.slice.size >= p - i) return false;
    if (o) {
        let t = e.tr.step(d);
        t.setSelection(u.create(t.doc, i));
        o(t.scrollIntoView())
    }
    return true
}

function x(e, t, r = false) {
    for (let n = e; n; n = t == "start" ? n.firstChild : n.lastChild) {
        if (n.isTextblock) return true;
        if (r && n.childCount != 1) return false
    }
    return false
}
const $ = (e, t, r) => {
    let {
        $head: n,
        empty: o
    } = e.selection, l = n;
    if (!o) return false;
    if (n.parent.isTextblock) {
        if (r ? !r.endOfTextblock("backward", e) : n.parentOffset > 0) return false;
        l = S(n)
    }
    let s = l && l.nodeBefore;
    if (!s || !a.isSelectable(s)) return false;
    t && t(e.tr.setSelection(a.create(e.doc, l.pos - s.nodeSize)).scrollIntoView());
    return true
};

function S(e) {
    if (!e.parent.type.spec.isolating)
        for (let t = e.depth - 1; t >= 0; t--) {
            if (e.index(t) > 0) return e.doc.resolve(e.before(t + 1));
            if (e.node(t).type.spec.isolating) break
        }
    return null
}

function I(e, t) {
    let {
        $cursor: r
    } = e.selection;
    return !r || (t ? !t.endOfTextblock("forward", e) : r.parentOffset < r.parent.content.size) ? null : r
}
const A = (e, r, n) => {
    let o = I(e, n);
    if (!o) return false;
    let l = T(o);
    if (!l) return false;
    let s = l.nodeAfter;
    if (G(e, l, r, 1)) return true;
    if (o.parent.content.size == 0 && (x(s, "start") || a.isSelectable(s))) {
        let n = t(e.doc, o.before(), o.after(), f.empty);
        if (n && n.slice.size < n.to - n.from) {
            if (r) {
                let t = e.tr.step(n);
                t.setSelection(x(s, "start") ? p.findFrom(t.doc.resolve(t.mapping.map(l.pos)), 1) : a.create(t.doc, t.mapping.map(l.pos)));
                r(t.scrollIntoView())
            }
            return true
        }
    }
    if (s.isAtom && l.depth == o.depth - 1) {
        r && r(e.tr.delete(l.pos, l.pos + s.nodeSize).scrollIntoView());
        return true
    }
    return false
};
const M = (e, t, r) => {
    let {
        $head: n,
        empty: o
    } = e.selection, l = n;
    if (!o) return false;
    if (n.parent.isTextblock) {
        if (r ? !r.endOfTextblock("forward", e) : n.parentOffset < n.parent.content.size) return false;
        l = T(n)
    }
    let s = l && l.nodeAfter;
    if (!s || !a.isSelectable(s)) return false;
    t && t(e.tr.setSelection(a.create(e.doc, l.pos)).scrollIntoView());
    return true
};

function T(e) {
    if (!e.parent.type.spec.isolating)
        for (let t = e.depth - 1; t >= 0; t--) {
            let r = e.node(t);
            if (e.index(t) + 1 < r.childCount) return e.doc.resolve(e.after(t + 1));
            if (r.type.spec.isolating) break
        }
    return null
}
const V = (e, t) => {
    let r, l = e.selection,
        s = l instanceof a;
    if (s) {
        if (l.node.isTextblock || !n(e.doc, l.from)) return false;
        r = l.from
    } else {
        r = o(e.doc, l.from, -1);
        if (r == null) return false
    }
    if (t) {
        let n = e.tr.join(r);
        s && n.setSelection(a.create(n.doc, r - e.doc.resolve(r).nodeBefore.nodeSize));
        t(n.scrollIntoView())
    }
    return true
};
const C = (e, t) => {
    let r, l = e.selection;
    if (l instanceof a) {
        if (l.node.isTextblock || !n(e.doc, l.to)) return false;
        r = l.to
    } else {
        r = o(e.doc, l.to, 1);
        if (r == null) return false
    }
    t && t(e.tr.join(r).scrollIntoView());
    return true
};
const z = (t, r) => {
    let {
        $from: n,
        $to: o
    } = t.selection;
    let l = n.blockRange(o),
        s = l && e(l);
    if (s == null) return false;
    r && r(t.tr.lift(l, s).scrollIntoView());
    return true
};
const B = (e, t) => {
    let {
        $head: r,
        $anchor: n
    } = e.selection;
    if (!r.parent.type.spec.code || !r.sameParent(n)) return false;
    t && t(e.tr.insertText("\n").scrollIntoView());
    return true
};

function v(e) {
    for (let t = 0; t < e.edgeCount; t++) {
        let {
            type: r
        } = e.edge(t);
        if (r.isTextblock && !r.hasRequiredAttrs()) return r
    }
    return null
}
const O = (e, t) => {
    let {
        $head: r,
        $anchor: n
    } = e.selection;
    if (!r.parent.type.spec.code || !r.sameParent(n)) return false;
    let o = r.node(-1),
        l = r.indexAfter(-1),
        s = v(o.contentMatchAt(l));
    if (!s || !o.canReplaceWith(l, l, s)) return false;
    if (t) {
        let n = r.after(),
            o = e.tr.replaceWith(n, n, s.createAndFill());
        o.setSelection(p.near(o.doc.resolve(n), 1));
        t(o.scrollIntoView())
    }
    return true
};
const R = (e, t) => {
    let r = e.selection,
        {
            $from: n,
            $to: o
        } = r;
    if (r instanceof d || n.parent.inlineContent || o.parent.inlineContent) return false;
    let l = v(o.parent.contentMatchAt(o.indexAfter()));
    if (!l || !l.isTextblock) return false;
    if (t) {
        let r = (!n.parentOffset && o.index() < o.parent.childCount ? n : o).pos;
        let s = e.tr.insert(r, l.createAndFill());
        s.setSelection(u.create(s.doc, r + 1));
        t(s.scrollIntoView())
    }
    return true
};
const D = (t, r) => {
    let {
        $cursor: n
    } = t.selection;
    if (!n || n.parent.content.size) return false;
    if (n.depth > 1 && n.after() != n.end(-1)) {
        let e = n.before();
        if (l(t.doc, e)) {
            r && r(t.tr.split(e).scrollIntoView());
            return true
        }
    }
    let o = n.blockRange(),
        s = o && e(o);
    if (s == null) return false;
    r && r(t.tr.lift(o, s).scrollIntoView());
    return true
};

function W(e) {
    return (t, r) => {
        let {
            $from: n,
            $to: o
        } = t.selection;
        if (t.selection instanceof a && t.selection.node.isBlock) {
            if (!n.parentOffset || !l(t.doc, n.pos)) return false;
            r && r(t.tr.split(n.pos).scrollIntoView());
            return true
        }
        if (!n.depth) return false;
        let s = [];
        let i, f, c = false,
            p = false;
        for (let t = n.depth;; t--) {
            let r = n.node(t);
            if (r.isBlock) {
                c = n.end(t) == n.pos + (n.depth - t);
                p = n.start(t) == n.pos - (n.depth - t);
                f = v(n.node(t - 1).contentMatchAt(n.indexAfter(t - 1)));
                let r = e && e(o.parent, c, n);
                s.unshift(r || (c && f ? {
                    type: f
                } : null));
                i = t;
                break
            }
            if (t == 1) return false;
            s.unshift(null)
        }
        let h = t.tr;
        (t.selection instanceof u || t.selection instanceof d) && h.deleteSelection();
        let m = h.mapping.map(n.pos);
        let k = l(h.doc, m, s.length, s);
        if (!k) {
            s[0] = f ? {
                type: f
            } : null;
            k = l(h.doc, m, s.length, s)
        }
        if (!k) return false;
        h.split(m, s.length, s);
        if (!c && p && n.node(i).type != f) {
            let e = h.mapping.map(n.before(i)),
                t = h.doc.resolve(e);
            f && n.node(i - 1).canReplaceWith(t.index(), t.index() + 1, f) && h.setNodeMarkup(h.mapping.map(n.before(i)), f)
        }
        r && r(h.scrollIntoView());
        return true
    }
}
const j = W();
const F = (e, t) => j(e, t && (r => {
    let n = e.storedMarks || e.selection.$to.parentOffset && e.selection.$from.marks();
    n && r.ensureMarks(n);
    t(r)
}));
const E = (e, t) => {
    let r, {
        $from: n,
        to: o
    } = e.selection;
    let l = n.sharedDepth(o);
    if (l == 0) return false;
    r = n.before(l);
    t && t(e.tr.setSelection(a.create(e.doc, r)));
    return true
};
const P = (e, t) => {
    t && t(e.tr.setSelection(new d(e.doc)));
    return true
};

function q(e, t, r) {
    let o = t.nodeBefore,
        l = t.nodeAfter,
        s = t.index();
    if (!o || !l || !o.type.compatibleContent(l.type)) return false;
    if (!o.content.size && t.parent.canReplace(s - 1, s)) {
        r && r(e.tr.delete(t.pos - o.nodeSize, t.pos).scrollIntoView());
        return true
    }
    if (!t.parent.canReplace(s, s + 1) || !(l.isTextblock || n(e.doc, t.pos))) return false;
    r && r(e.tr.join(t.pos).scrollIntoView());
    return true
}

function G(t, r, o, l) {
    let i, a, u = r.nodeBefore,
        d = r.nodeAfter;
    let h = u.type.spec.isolating || d.type.spec.isolating;
    if (!h && q(t, r, o)) return true;
    let m = !h && r.parent.canReplace(r.index(), r.index() + 1);
    if (m && (i = (a = u.contentMatchAt(u.childCount)).findWrapping(d.type)) && a.matchType(i[0] || d.type).validEnd) {
        if (o) {
            let e = r.pos + d.nodeSize,
                l = c.empty;
            for (let e = i.length - 1; e >= 0; e--) l = c.from(i[e].create(null, l));
            l = c.from(u.copy(l));
            let a = t.tr.step(new s(r.pos - 1, e, r.pos, e, new f(l, 1, 0), i.length, true));
            let p = a.doc.resolve(e + 2 * i.length);
            p.nodeAfter && p.nodeAfter.type == u.type && n(a.doc, p.pos) && a.join(p.pos);
            o(a.scrollIntoView())
        }
        return true
    }
    let k = d.type.spec.isolating || l > 0 && h ? null : p.findFrom(r, 1);
    let g = k && k.$from.blockRange(k.$to),
        y = g && e(g);
    if (y != null && y >= r.depth) {
        o && o(t.tr.lift(g, y).scrollIntoView());
        return true
    }
    if (m && x(d, "start", true) && x(u, "end")) {
        let e = u,
            n = [];
        for (;;) {
            n.push(e);
            if (e.isTextblock) break;
            e = e.lastChild
        }
        let l = d,
            i = 1;
        for (; !l.isTextblock; l = l.firstChild) i++;
        if (e.canReplace(e.childCount, e.childCount, l.content)) {
            if (o) {
                let e = c.empty;
                for (let t = n.length - 1; t >= 0; t--) e = c.from(n[t].copy(e));
                let l = t.tr.step(new s(r.pos - n.length, r.pos + d.nodeSize, r.pos + i, r.pos + d.nodeSize - i, new f(e, n.length, 0), 0, true));
                o(l.scrollIntoView())
            }
            return true
        }
    }
    return false
}

function H(e) {
    return function(t, r) {
        let n = t.selection,
            o = e < 0 ? n.$from : n.$to;
        let l = o.depth;
        while (o.node(l).isInline) {
            if (!l) return false;
            l--
        }
        if (!o.node(l).isTextblock) return false;
        r && r(t.tr.setSelection(u.create(t.doc, e < 0 ? o.start(l) : o.end(l))));
        return true
    }
}
const N = H(-1);
const J = H(1);

function K(e, t = null) {
    return function(r, n) {
        let {
            $from: o,
            $to: l
        } = r.selection;
        let s = o.blockRange(l),
            f = s && i(s, e, t);
        if (!f) return false;
        n && n(r.tr.wrap(s, f).scrollIntoView());
        return true
    }
}

function L(e, t = null) {
    return function(r, n) {
        let o = false;
        for (let n = 0; n < r.selection.ranges.length && !o; n++) {
            let {
                $from: {
                    pos: l
                },
                $to: {
                    pos: s
                }
            } = r.selection.ranges[n];
            r.doc.nodesBetween(l, s, ((n, l) => {
                if (o) return false;
                if (n.isTextblock && !n.hasMarkup(e, t))
                    if (n.type == e) o = true;
                    else {
                        let t = r.doc.resolve(l),
                            n = t.index();
                        o = t.parent.canReplaceWith(n, n + 1, e)
                    }
            }))
        }
        if (!o) return false;
        if (n) {
            let o = r.tr;
            for (let n = 0; n < r.selection.ranges.length; n++) {
                let {
                    $from: {
                        pos: l
                    },
                    $to: {
                        pos: s
                    }
                } = r.selection.ranges[n];
                o.setBlockType(l, s, e, t)
            }
            n(o.scrollIntoView())
        }
        return true
    }
}

function Q(e, t, r, n) {
    for (let o = 0; o < t.length; o++) {
        let {
            $from: l,
            $to: s
        } = t[o];
        let i = l.depth == 0 && (e.inlineContent && e.type.allowsMarkType(r));
        e.nodesBetween(l.pos, s.pos, ((e, t) => {
            if (i || !n && e.isAtom && e.isInline && t >= l.pos && t + e.nodeSize <= s.pos) return false;
            i = e.inlineContent && e.type.allowsMarkType(r)
        }));
        if (i) return true
    }
    return false
}

function U(e) {
    let t = [];
    for (let r = 0; r < e.length; r++) {
        let {
            $from: n,
            $to: o
        } = e[r];
        n.doc.nodesBetween(n.pos, o.pos, ((e, r) => {
            if (e.isAtom && e.content.size && e.isInline && r >= n.pos && r + e.nodeSize <= o.pos) {
                r + 1 > n.pos && t.push(new h(n, n.doc.resolve(r + 1)));
                n = n.doc.resolve(r + 1 + e.content.size);
                return false
            }
        }));
        n.pos < o.pos && t.push(new h(n, o))
    }
    return t
}

function X(e, t = null, r) {
    let n = (r && r.removeWhenPresent) !== false;
    let o = (r && r.enterInlineAtoms) !== false;
    let l = !(r && r.includeWhitespace);
    return function(r, s) {
        let {
            empty: i,
            $cursor: f,
            ranges: c
        } = r.selection;
        if (i && !f || !Q(r.doc, c, e, o)) return false;
        if (s)
            if (f) e.isInSet(r.storedMarks || f.marks()) ? s(r.tr.removeStoredMark(e)) : s(r.tr.addStoredMark(e.create(t)));
            else {
                let i, f = r.tr;
                o || (c = U(c));
                i = n ? !c.some((t => r.doc.rangeHasMark(t.$from.pos, t.$to.pos, e))) : !c.every((t => {
                    let r = false;
                    f.doc.nodesBetween(t.$from.pos, t.$to.pos, ((n, o, l) => {
                        if (r) return false;
                        r = !e.isInSet(n.marks) && !!l && l.type.allowsMarkType(e) && !(n.isText && /^\s*$/.test(n.textBetween(Math.max(0, t.$from.pos - o), Math.min(n.nodeSize, t.$to.pos - o))))
                    }));
                    return !r
                }));
                for (let r = 0; r < c.length; r++) {
                    let {
                        $from: n,
                        $to: o
                    } = c[r];
                    if (i) {
                        let r = n.pos,
                            s = o.pos,
                            i = n.nodeAfter,
                            c = o.nodeBefore;
                        let a = l && i && i.isText ? /^\s*/.exec(i.text)[0].length : 0;
                        let p = l && c && c.isText ? /\s*$/.exec(c.text)[0].length : 0;
                        if (r + a < s) {
                            r += a;
                            s -= p
                        }
                        f.addMark(r, s, e.create(t))
                    } else f.removeMark(n.pos, o.pos, e)
                }
                s(f.scrollIntoView())
            } return true
    }
}

function Y(e, t) {
    return r => {
        if (!r.isGeneric) return e(r);
        let o = [];
        for (let e = 0; e < r.mapping.maps.length; e++) {
            let t = r.mapping.maps[e];
            for (let e = 0; e < o.length; e++) o[e] = t.map(o[e]);
            t.forEach(((e, t, r, n) => o.push(r, n)))
        }
        let l = [];
        for (let e = 0; e < o.length; e += 2) {
            let n = o[e],
                s = o[e + 1];
            let i = r.doc.resolve(n),
                f = i.sharedDepth(s),
                c = i.node(f);
            for (let e = i.indexAfter(f), r = i.after(f + 1); r <= s; ++e) {
                let n = c.maybeChild(e);
                if (!n) break;
                if (e && l.indexOf(r) == -1) {
                    let o = c.child(e - 1);
                    o.type == n.type && t(o, n) && l.push(r)
                }
                r += n.nodeSize
            }
        }
        l.sort(((e, t) => e - t));
        for (let e = l.length - 1; e >= 0; e--) n(r.doc, l[e]) && r.join(l[e]);
        e(r)
    }
}

function Z(e, t) {
    let r = Array.isArray(t) ? e => t.indexOf(e.type.name) > -1 : t;
    return (t, n, o) => e(t, n && Y(n, r), o)
}

function _(...e) {
    return function(t, r, n) {
        for (let o = 0; o < e.length; o++)
            if (e[o](t, r, n)) return true;
        return false
    }
}
let ee = _(m, g, $);
let te = _(m, A, M);
const re = {
    Enter: _(B, R, D, j),
    "Mod-Enter": O,
    Backspace: ee,
    "Mod-Backspace": ee,
    "Shift-Backspace": ee,
    Delete: te,
    "Mod-Delete": te,
    "Mod-a": P
};
const ne = {
    "Ctrl-h": re.Backspace,
    "Alt-Backspace": re["Mod-Backspace"],
    "Ctrl-d": re.Delete,
    "Ctrl-Alt-Backspace": re["Mod-Delete"],
    "Alt-Delete": re["Mod-Delete"],
    "Alt-d": re["Mod-Delete"],
    "Ctrl-a": N,
    "Ctrl-e": J
};
for (let e in re) ne[e] = re[e];
const oe = typeof navigator != "undefined" ? /Mac|iP(hone|[oa]d)/.test(navigator.platform) : !(typeof os == "undefined" || !os.platform) && os.platform() == "darwin";
const le = oe ? ne : re;
export {
    Z as autoJoin, le as baseKeymap, _ as chainCommands, R as createParagraphNear, m as deleteSelection, O as exitCode, g as joinBackward, C as joinDown, A as joinForward, y as joinTextblockBackward, w as joinTextblockForward, V as joinUp, z as lift, D as liftEmptyBlock, ne as macBaseKeymap, B as newlineInCode, re as pcBaseKeymap, P as selectAll, $ as selectNodeBackward, M as selectNodeForward, E as selectParentNode, J as selectTextblockEnd, N as selectTextblockStart, L as setBlockType, j as splitBlock, W as splitBlockAs, F as splitBlockKeepMarks, X as toggleMark, K as wrapIn
};