---
date: {{date}}
tags: []
---

# {{date}}

Append-only log. Each entry uses the format:

```
## HH:MM - [agent-name] - short summary
- detail
- detail with [[backlinks]]
```

Multiple agents and Cowork sessions can write here on the same day. Each
write is one atomic block - never edit a previous block, only append new
ones below.

---
