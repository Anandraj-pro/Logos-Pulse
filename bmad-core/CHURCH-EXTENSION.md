# BMAD Church Extension — Logos Pulse

This extension adds church leadership agents, Bible knowledge, and pastoral
task support to the standard BMAD Method framework.

## What Was Added

### Agents (`agents/`)
| File | Role | Authority |
|---|---|---|
| `bishop.md` | Bishop | Highest — diocese/region oversight |
| `sr-pastor.md` | Senior Pastor | Church-level vision and leadership |
| `pastor.md` | Pastor | Direct member care and daily tracking |

### Personas (`personas/`)
| File | Contents |
|---|---|
| `church-personas.md` | Bishop, Sr. Pastor, Pastor, Prayer Warrior personas + escalation paths |

### Knowledge Base (`knowledge/`)
| File | Contents |
|---|---|
| `bible-knowledge.md` | All 66 books with themes, key passages by discipline (prayer, Bible reading, growth, confession, worship), reading plans, pastoral wisdom, liturgical calendar, doctrinal reference |

### Updated Files
| File | Change |
|---|---|
| `agents/bmad-orchestrator.md` | Added agent routing table with church agents + `church-mode` command |
| `tasks/task-registry.md` | Added Bishop, Sr. Pastor, Pastor, and Bible Knowledge task sets |

## Role Hierarchy

```
Admin (Raju@002)
  └── Bishop (Bishop@123)
        └── Sr. Pastor
              └── Pastor (Pastor@123)
                    └── Prayer Warrior (Open@123)
```

## How to Use

### Switch to a church agent
In the orchestrator, type: `switch bishop`, `switch sr-pastor`, or `switch pastor`

### Look up a Bible passage
Consult `knowledge/bible-knowledge.md` directly, or run `passage-lookup` task

### Plan a sermon series
Use the `sr-pastor` agent with command: `sermon-series [theme]`

### Review a pastor's congregation
Use the `bishop` agent with command: `review-pastor [pastor_id]`

### Review member care
Use the `pastor` agent with command: `group-summary` or `member-report [id]`

## Data Authority Matrix

| Role | Can See |
|---|---|
| Bishop | All pastors + all prayer warriors in diocese |
| Sr. Pastor | All pastors + all members in own church |
| Pastor | Only own assigned prayer warriors |
| Prayer Warrior | Only own data |

This mirrors the RLS (Row Level Security) setup in Supabase via `can_view_user()`.
