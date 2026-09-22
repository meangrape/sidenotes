-- pandoc Lua filter (HTML only): turn each footnote into an inline sidenote.
-- The reference mark and the note body are emitted side by side in the flow,
-- so CSS can float the body into the margin, level with the mark.
if not FORMAT:match("html") then return {} end

function Note(el)
  local ref  = pandoc.Span({}, {class = "sidenote-ref"})
  local body = pandoc.utils.blocks_to_inlines(el.content, {pandoc.LineBreak()})
  local note = pandoc.Span(body, {class = "sidenote"})
  return {ref, note}
end
