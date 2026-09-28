# Science critique — attention-weaving r06 · machine learning (transformer attention, softmax) · 2026-09-28
render: ~/Downloads/pp_attention_weaving_iterate_v16.png (gcode: ~/Downloads/pp_attention_weaving_iterate_v16.gcode, seed 7, 24x30 portrait, 15 693 cmds, 5 pens)

Pass 2. There is still **no `dossier.md` and no `encoding.md`** (S5), so there are no §7 check numbers and no §4 lies list to grade against. The check numbers below are the claims printed in the footer, each recomputed from the geometry the sheet itself draws. The lies list is the BRIEF "What must be TRUE" list plus the open S mandates.

How it was measured: from the gcode only.
- Strands were rebuilt by bridging each fragment across its over/under gaps. That gives 22 Q + 1 extra Q11 pass, 16 K, 16 V and 22 Z.
- The hill is the innermost black profile pass. It was integrated over 16 equal bins across the slit, x 66.66 → 140.34.

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| Σa | — (footer "Σa = 1") | 1.000000 from the per-bin hill areas | the profile area partitions exactly (no cumulative curve drawn any more) | OK |
| a_max | — ("a MAX 0.190") | 0.18997, key 5 | hill peak 20.72 mm at x = 88.25, inside bin 5 [85.08, 89.69] | OK |
| H | — ("H 3.76 / 4.00 BITS") | 3.7625 of log2 16 = 4.000 | from the hill areas | OK |
| per-key a | — | [.038 .045 .051 .066 **.190 .139** .079 .056 .054 .046 .045 .044 .041 .037 .036 .034] | ∫ per equal bin / total | — |
| bins | — ("16 EQUAL BINS OF 4.60 MM") | 73.68 / 16 = 4.605 | slit x 66.66 → 140.34 | OK |
| slit | — ("SLIT 73.7 MM") | 73.68 | wall gap | OK |
| hill height ∝ a | S2 | peak/median a = 4.164 | peak/median bin-mean height = 4.164 | OK (exact) |
| counts | — ("22 Q · 16 K → 22 Z") | n_Z = n_Q | 22 Q reach the hill (Q11 double-passed, 0.34 mm), 16 K end on the hill, 22 Z leave the wall at y = 183.6 | OK |
| Z lanes per bin | S2 | largest-remainder apportionment of 22·a = [1,1,1,1,4,3,2,1,1,1,1,1,1,1,1,1] | Z starts at the wall: [1,1,1,1,4,3,2,1,1,1,1,1,1,1,1,1] | OK |
| Q lanes per bin | S2 | same [1,1,1,1,4,3,2,1,…] | Q ends on the hill: **[1,1,1,4,2,2,2,1,1,1,1,1,1,1,1,1]** | **off by one bin at the peak** |
| K_j → bin j | S3 | 16/16 | K ends at x 69.0, 73.6, 78.2, … 133.4, 138.0, every one within 0.05 mm of its bin centre | OK |
| min pitch | — ("MIN PITCH 0.90 MM") | — | green lateral minimum 0.898 mm at (98.6, 158.9), no pair below 0.89. Crimson 1.26 mm (excluding the intended Q11 double). Gold 1.08 mm. Blue has no parallel pair under 1.5 mm | OK |
| "GOLD OVER GREEN WHERE a > 1/16" | — | on row Q11, a > 1/16 for keys {4, 5, 6, 7} | Q11's output lane (wall x = 103.18, exit y = 104.1): gold is over at exactly the 4 V strands from left-reed y = 159.8 / 157.2 / 154.6 / 152.0, which are keys 4–7 counting from the top. Green is over everywhere else | OK on the one checkable row. The other 21 rows (302 − 4 crossings) have no stated A, so they cannot be verified |
| ink-on-ink crossings | — | 0 | V×Z 0, Q×K 0 (over/under is real everywhere). Q/K × hill 0 | OK |

## Lies list
| item | status |
|---|---|
| Everything passes through the waist | clean. All 22 Q and all 16 K terminate on the hill. All 22 Z are born at the wall. Nothing is born mid-sheet. |
| n_Z = n_Q (S1: keys are consumed, not output) | clean |
| Over/under is real | clean. There are 0 drawn crossings in any layer pair. V×Z: gold over 115, green over 187. |
| Softmax normalises, peaked | clean. Equal bins, so both area and height are true. |
| V joins after the waist | clean. All gold ink is at y ≤ 177.1, below the wall at 183.6. All 16 V strands are born at left-reed ticks, and 0 gold fragments are shorter than 5 mm. |
| Emphasis means one thing | clean. The only doubled coloured line is Q11, and it is labelled "Q11 · ITS ROW IS THE HILL". The cumulative curve and "1.000" are gone. |
| Captions true | clean. All 8 footer numbers match the measurements. |
| **A lane is one query** | **VIOLATED** (slit, x 66.7–140.3). The footer says each lane is a query ("22 Q → 22 Z"). But the lane positions in the slit are Q11's row cut into 22 quanta. So 4 different queries pass through key 5 because of Q11's weights, and a lane's position says nothing about its own query's row. Z11 itself leaves at x = 103.18 (bin 8), while its own row's centroid Σa_j·x_j is **98.54 mm** (bin 7). This comes from my own r04 S1 + S2 wording; see mandate 1. |
| Every Z exit ticked | **VIOLATED (1/22).** The Z lane that starts at wall x = 72.77 dies under the "Z = AV" label at (221.0, 48.9), 8.7 mm short of the frame, with no tick. The other 21 exits each have a tick. |
| Q lands where its Z leaves | **VIOLATED (3/22).** Q lanes 5–7 end at x = 83.4 / 84.1 / 84.8 on the left flank (bin 4, a = .066). Their Z continuations start at 85.33 / 86.41 / 87.49 (bin 5). |

## Scores
- **truth 7**: every printed number is exact to the stated precision. Keys are consumed (S1), K identity is exact (S3), and the over/under rule is exactly right on the one row that is on the sheet. What is left is a conceptual conflation. The 22 lanes are asserted to be 22 queries, but they are placed by one query's weights. On top of that, 302 over/under decisions rest on 21 attention rows that exist nowhere: no dossier, no caption.
- **encoding fidelity 7**: the hill is now exact in both area and height (4.164 = 4.164). Z per bin is the exact apportionment, and pitch and slit are exact. But the Q channel lands its densest pile-up on bin 4 (4 ends against 1 expected) instead of bin 5 (2 against 4). One Z lane dies at the label. The hill has no A axis (S6).
- **insight legibility 7**: "SUMS TO ONE", the equal-bin hill and Q11's label land for a stranger, and the footer now decodes. However, the one row that demonstrates "GOLD OVER GREEN WHERE a > 1/16" cannot be found on the sheet. Q11's output lane is a single green pass identical to the other 21, and the V reed carries no key index. So neither a scientist nor a stranger can check the rule the caption states. Without a dossier §5, no misconception correction is identifiable.
- **VERDICT: FAIL**

## Mandates
1. **Lane identity at the slit** (x 66.66–140.34, y 183.6).
   - Measured: Z starts per bin = [1,1,1,1,4,3,2,1,…], which is Q11's row apportioned into 22 quanta. But the footer says each lane is a query. Z11 (wall x = 103.18) leaves from bin 8, while its own row's centroid Σ a_j·x_j = **98.54 mm** (bin 7).
   - Expected: each Z_i leaves the slit at its own row's centroid, Σ_j A_ij·x_j. AV is a convex combination, so the lane's position is then the weighted average of the key positions. That puts Z11 at 98.54 mm.
   - For this, the 22×16 A that also drives the 302 other over/under crossings must be written into `encoding.md` (closes S5).
   - The only alternative is to drop "22 Q → 22 Z" and caption the lanes as "Q11's row in 22 quanta".
   - This supersedes the lane clause of my r04 S2.
2. **Q lands where its Z leaves** (hill left flank, x 81–90, y 191–206).
   - Measured: Q ends per bin = [1,1,1,4,2,2,2,1,…].
   - Q strands 5–7 terminate at x = 83.4 / 84.1 / 84.8, inside bin 4 (a = .066). That is 0.3–1.7 mm left of bin 5's edge at 85.08 and 1.9–2.7 mm left of their Z continuations at 85.33 / 86.41 / 87.49.
   - Expected: each Q_i terminates in the same bin its Z_i leaves from (|x_Q − x_Z| ≤ 0.5 mm). Under mandate 1(a) that means the same centroid.
3. **Make the stated rule checkable, and close the last exit** (rope and right reed).
   - Measured: "GOLD OVER GREEN WHERE a > 1/16" holds exactly on Q11's output lane (gold over at V reed y = 159.8 / 157.2 / 154.6 / 152.0 = keys 4–7). But that lane (wall x = 103.18 → exit y = 104.1) is a single pass indistinguishable from the other 21, and the V reed (x = 10.3, y 128.5–167.7) carries no key index.
   - Measured: the Z lane from wall x = 72.77 ends at (221.0, 48.9) under the "Z = AV" label, with no tick (21/22 ticked).
   - Expected: label Z11 at its exit tick (y = 104.1), and index the V reed (1 at y = 167.7 down to 16 at y = 128.5, or mark keys 4–7). Route the x = 72.77 lane to x = 229.7 with a tick, moving the label rather than cutting the lane.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S1 | FIXED | 22 Z are born at the wall and 16 K terminate on the hill. The footer reads "22 Q · 16 K → 22 Z". |
| S2 | PARTIAL | Equal bins of 4.605 mm. Hill peak/median height = 4.164 = a peak/median (was 2.09 vs 4.21). Z per bin = the exact largest-remainder apportionment. But Q ends per bin are [1,1,1,4,2,2,2,…], not [1,1,1,1,4,3,2,…] (mandate 2). The lane clause itself is superseded by mandate 1. |
| S3 | FIXED | K per bin = 16 × 1 (was [1,1,1,0,1,2,2,…]). Every K ends ≤ 0.05 mm from its bin centre. Every K starts at a reed tick: 5 top, 11 right. The one at (62.7, 287.2) stops under a Q, 2.5 mm below its tick at x = 64.5. |
| S4 | FIXED | "MIN PITCH 0.90" against a measured 0.898 mm (was 0.90 printed vs 0.75). "SCORES CROSS" and "NONE MASKED" are gone. "Σa = 1" is printed without false precision. |
| S5 | NOT FIXED | There is still no `dossier.md` or `encoding.md`. This now blocks verifying 302 of the 322 V×Z over/under decisions (mandate 1). |
| S6 | NOT FIXED (deferred) | The hill has no A axis. With the cumulative curve gone, "a MAX 0.190" lives only in the footer, and no tick on the peak ties it to the hill. |
| S7 | dropped (r05 not continued) | — |
| A7 / A8 / A9 (science-relevant parts) | A7: 16/16 V start at left-reed ticks and end 0.86–1.29 mm from the top Z lane, with 0 gold pieces under 5 mm. A8: K 16/16 ticked, Z 21/22 ticked. A9: the cumulative curve and "1.000" are removed, blue and gold are single-pass, and the only doubled line is the labelled Q11 | — |

Regressions: none. Every truth that held in r04 still holds: Σa, a_max, H, over/under, and V strictly below the wall.
