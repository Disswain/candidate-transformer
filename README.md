# Candidate Data Transformer

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)]()
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()


A production-style ETL pipeline that extracts, normalizes, validates, merges, and projects candidate information from multiple heterogeneous sources into a single canonical candidate profile - complete with confidence scoring and field-level provenance tracking.

---

## Table of Contents

- [Why This Exists](#why-this-exists)
- [Features](#features)
- [Pipeline Architecture](#pipeline-architecture)
- [Project Structure](#project-structure)
- [Source Priority](#source-priority)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Running Tests](#running-tests)
- [Sample Output](#sample-output)
- [Configuration](#configuration)
- [Design Decisions](#design-decisions)
- [Assumptions](#assumptions)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Why This Exists

Recruitment systems pull candidate data from a patchwork of sources — recruiter spreadsheets, ATS exports, LinkedIn, GitHub, and resumes in half a dozen formats. Every source has its own structure, its own quirks, and its own blind spots. This project takes that mess and turns it into one clean, validated, deduplicated JSON profile per candidate — with full traceability back to where every field came from.

---

## Features

**Multi-source extraction**
- Recruiter CSV
- ATS JSON
- LinkedIn Profile
- GitHub Profile
- Resume (TXT)
- Resume (PDF)

**Normalization**
- Names · Emails · Phone numbers (E.164) · Countries (ISO-3166) · Skills · Dates · URLs

**Merging & deduplication**
- Configurable source-priority resolution
- Deduplicates emails, phone numbers, skills, experience, and education entries

**Trust & traceability**
- Per-field confidence scoring
- Full provenance tracking for every extracted value

**Output**
- Schema-validated canonical profile
- Configurable JSON projection
- Automated unit test suite

---

## Pipeline Architecture

```
Input Sources
      │
      ▼
  Extractors          (source-specific parsing)
      │
      ▼
IntermediateCandidate  (raw, unnormalized representation)
      │
      ▼
  Normalization        (formats, units, casing)
      │
      ▼
Canonical Candidate
      │
      ▼
  Validation           (schema + business rules)
      │
      ▼
  Merge Resolver        (source-priority conflict resolution)
      │
      ▼
Confidence Calculator
      │
      ▼
  Projection Layer      (configurable output schema)
      │
      ▼
  Output JSON
```

{"type":"excalidraw/clipboard","workspaceId":"QSTrzMMZGpoI84zPBm1W","elements":[{"0":525,"1":340,"renderVersion":"20260630","strokeColor":"#d7d9dc","fillStyle":"solid","backgroundColor":"transparent","strokeWidth":1,"strokeStyle":"solid","roughness":1,"opacity":100,"strokeSharpness":"sharp","version":51,"isDeleted":false,"id":"O1r0teKRzQDDxw1Q17ym","code":"","x":25,"y":25,"diagramType":"freeform-diagram","forceAiMode":false,"isBeingGenerated":false,"lastEditMode":"ai","scale":1,"type":"diagram","width":2524,"height":550,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":899726398,"zIndex":0,"title":"Candidate Data Processing Pipeline","modifiedAt":1782853111415,"isSyntaxMissing":false},{"strokeColor":"#1c1c1c","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","strokeSharpness":"round","opacity":100,"roughness":1,"shouldApplyRoughness":true,"isDeleted":false,"diagramId":"O1r0teKRzQDDxw1Q17ym","figureId":null,"id":"d37c9b44c9b9fe1827d03f5a62beaaab","x":40,"y":40,"diagramEntityId":"g_inputs","isContainer":true,"sizingMode":"manual","freeform":{"tag":"Group","title":{"text":"Input Sources","icon":"database","width":"full","hAlign":"center"},"bgColor":"#E8F4FD","borderColor":"#4A90E2"},"compound":{"type":"parent","containerType":"freeform"},"type":"freeform","width":220,"height":520,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":1958533410,"version":1,"zIndex":1},{"strokeColor":"#1c1c1c","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","strokeSharpness":"round","opacity":100,"roughness":1,"shouldApplyRoughness":true,"isDeleted":false,"diagramId":"O1r0teKRzQDDxw1Q17ym","containerId":"d37c9b44c9b9fe1827d03f5a62beaaab","figureId":null,"id":"90b13c2753db24964ae5ae5e9919f97c","x":125,"y":110,"diagramEntityId":"src_csv","isContainer":false,"freeform":{"tag":"Icon","icon":"file-spreadsheet","texts":[{"text":"CSV"}]},"compound":{"type":"parent","containerType":"freeform"},"type":"freeform","width":50,"height":50,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":1693598206,"version":1,"zIndex":2},{"strokeColor":"#1c1c1c","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","strokeSharpness":"round","opacity":100,"roughness":1,"shouldApplyRoughness":true,"isDeleted":false,"diagramId":"O1r0teKRzQDDxw1Q17ym","containerId":"d37c9b44c9b9fe1827d03f5a62beaaab","figureId":null,"id":"af0abb5e9af055fb0ec46cfa903d2181","x":125,"y":195,"diagramEntityId":"src_ats","isContainer":false,"freeform":{"tag":"Icon","icon":"file-json","texts":[{"text":"ATS JSON"}]},"compound":{"type":"parent","containerType":"freeform"},"type":"freeform","width":50,"height":50,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":1271489762,"version":1,"zIndex":3},{"strokeColor":"#1c1c1c","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","strokeSharpness":"round","opacity":100,"roughness":1,"shouldApplyRoughness":true,"isDeleted":false,"diagramId":"O1r0teKRzQDDxw1Q17ym","containerId":"d37c9b44c9b9fe1827d03f5a62beaaab","figureId":null,"id":"aa795303b80d21eaa282969cb1075809","x":125,"y":285,"diagramEntityId":"src_linkedin","isContainer":false,"freeform":{"tag":"Icon","icon":"linkedin","texts":[{"text":"LinkedIn"}]},"compound":{"type":"parent","containerType":"freeform"},"type":"freeform","width":50,"height":50,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":999641662,"version":1,"zIndex":4},{"strokeColor":"#1c1c1c","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","strokeSharpness":"round","opacity":100,"roughness":1,"shouldApplyRoughness":true,"isDeleted":false,"diagramId":"O1r0teKRzQDDxw1Q17ym","containerId":"d37c9b44c9b9fe1827d03f5a62beaaab","figureId":null,"id":"8066591ed386cb3f1d4de141fd1fe0bb","x":125,"y":375,"diagramEntityId":"src_github","isContainer":false,"freeform":{"tag":"Icon","icon":"github","texts":[{"text":"GitHub"}]},"compound":{"type":"parent","containerType":"freeform"},"type":"freeform","width":50,"height":50,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":1892579490,"version":1,"zIndex":5},{"strokeColor":"#1c1c1c","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","strokeSharpness":"round","opacity":100,"roughness":1,"shouldApplyRoughness":true,"isDeleted":false,"diagramId":"O1r0teKRzQDDxw1Q17ym","containerId":"d37c9b44c9b9fe1827d03f5a62beaaab","figureId":null,"id":"e25fa1d9e08301e304b0b393f6455e39","x":125,"y":465,"diagramEntityId":"src_resume","isContainer":false,"freeform":{"tag":"Icon","icon":"file-text","texts":[{"text":"Resume"}]},"compound":{"type":"parent","containerType":"freeform"},"type":"freeform","width":50,"height":50,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":602692222,"version":1,"zIndex":6},{"strokeColor":"#1c1c1c","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","strokeSharpness":"round","opacity":100,"roughness":1,"shouldApplyRoughness":true,"isDeleted":false,"diagramId":"O1r0teKRzQDDxw1Q17ym","figureId":null,"id":"5447d1bac1d338838bb67331a38bb20a","x":320,"y":260,"diagramEntityId":"extractors","isContainer":false,"freeform":{"tag":"Shape","shape":"rectangle","texts":[{"text":"Extractors","fontSize":16},{"text":"source-specific parsing","fontSize":12,"color":"gray"}],"icon":"scan-line","bgColor":"#FFF4E0","borderColor":"#E2A04A"},"compound":{"type":"parent","containerType":"freeform"},"type":"freeform","width":183.45123782753944,"height":90,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":595268706,"version":1,"zIndex":7},{"strokeColor":"#1c1c1c","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","strokeSharpness":"round","opacity":100,"roughness":1,"shouldApplyRoughness":true,"isDeleted":false,"diagramId":"O1r0teKRzQDDxw1Q17ym","figureId":null,"id":"a0af5be08cd21090dd4c98d645b42352","x":563,"y":255,"diagramEntityId":"intermediate","isContainer":false,"freeform":{"tag":"Shape","shape":"document","texts":[{"text":"IntermediateCandidate","fontSize":15},{"text":"raw, unnormalized","fontSize":12,"color":"gray"}],"bgColor":"#F0E8FD","borderColor":"#7A4AE2"},"compound":{"type":"parent","containerType":"freeform"},"type":"freeform","width":190,"height":100,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":884497086,"version":1,"zIndex":9},{"strokeColor":"#1c1c1c","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","strokeSharpness":"round","opacity":100,"roughness":1,"shouldApplyRoughness":true,"isDeleted":false,"diagramId":"O1r0teKRzQDDxw1Q17ym","figureId":null,"id":"1e61449f2f81af4711d2aa00f1eed77d","x":813,"y":260,"diagramEntityId":"normalize","isContainer":false,"freeform":{"tag":"Shape","shape":"rectangle","texts":[{"text":"Normalization","fontSize":16},{"text":"formats, units, casing","fontSize":12,"color":"gray"}],"icon":"sliders-horizontal","bgColor":"#FFF4E0","borderColor":"#E2A04A"},"compound":{"type":"parent","containerType":"freeform"},"type":"freeform","width":180,"height":90,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":1436432418,"version":1,"zIndex":11},{"strokeColor":"#1c1c1c","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","strokeSharpness":"round","opacity":100,"roughness":1,"shouldApplyRoughness":true,"isDeleted":false,"diagramId":"O1r0teKRzQDDxw1Q17ym","figureId":null,"id":"1adb42fe3eb967c7cf5eb3bee6f85cff","x":1053,"y":255,"diagramEntityId":"canonical","isContainer":false,"freeform":{"tag":"Shape","shape":"document","texts":[{"text":"CanonicalCandidate","fontSize":15},{"text":"normalized form","fontSize":12,"color":"gray"}],"bgColor":"#F0E8FD","borderColor":"#7A4AE2"},"compound":{"type":"parent","containerType":"freeform"},"type":"freeform","width":190,"height":100,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":77222654,"version":1,"zIndex":13},{"strokeColor":"#1c1c1c","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","strokeSharpness":"round","opacity":100,"roughness":1,"shouldApplyRoughness":true,"isDeleted":false,"diagramId":"O1r0teKRzQDDxw1Q17ym","figureId":null,"id":"7903a74e9b083e1f71631905da7b7a74","x":1303,"y":260,"diagramEntityId":"validation","isContainer":false,"freeform":{"tag":"Shape","shape":"rectangle","texts":[{"text":"Validation","fontSize":16},{"text":"schema & business rules","fontSize":12,"color":"gray"}],"icon":"shield-check","bgColor":"#FFF4E0","borderColor":"#E2A04A"},"compound":{"type":"parent","containerType":"freeform"},"type":"freeform","width":190.9252768953641,"height":90,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":1730601954,"version":1,"zIndex":15},{"strokeColor":"#1c1c1c","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","strokeSharpness":"round","opacity":100,"roughness":1,"shouldApplyRoughness":true,"isDeleted":false,"diagramId":"O1r0teKRzQDDxw1Q17ym","figureId":null,"id":"adce85252544e261102fb9c1ba660342","x":1554,"y":250,"diagramEntityId":"merge","isContainer":false,"freeform":{"tag":"Shape","shape":"rectangle","texts":[{"text":"Merge Resolver","fontSize":16},{"text":"source-priority conflict","fontSize":12,"color":"gray"},{"text":"resolution & dedup","fontSize":12,"color":"gray"}],"icon":"git-merge","bgColor":"#FFF4E0","borderColor":"#E2A04A"},"compound":{"type":"parent","containerType":"freeform"},"type":"freeform","width":200,"height":110,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":773014334,"version":1,"zIndex":17},{"strokeColor":"#1c1c1c","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","strokeSharpness":"round","opacity":100,"roughness":1,"shouldApplyRoughness":true,"isDeleted":false,"diagramId":"O1r0teKRzQDDxw1Q17ym","figureId":null,"id":"39be32a95b8598f259f26ec919508766","x":1814,"y":255,"diagramEntityId":"confidence","isContainer":false,"freeform":{"tag":"Shape","shape":"rectangle","texts":[{"text":"Confidence Calculator","fontSize":15},{"text":"scoring & ranking","fontSize":12,"color":"gray"}],"icon":"gauge","bgColor":"#FFF4E0","borderColor":"#E2A04A"},"compound":{"type":"parent","containerType":"freeform"},"type":"freeform","width":200,"height":100,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":1646532514,"version":1,"zIndex":19},{"strokeColor":"#1c1c1c","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","strokeSharpness":"round","opacity":100,"roughness":1,"shouldApplyRoughness":true,"isDeleted":false,"diagramId":"O1r0teKRzQDDxw1Q17ym","figureId":null,"id":"818c0070d4da9fc5d1be43aff9cadd01","x":2074,"y":255,"diagramEntityId":"projection","isContainer":false,"freeform":{"tag":"Shape","shape":"rectangle","texts":[{"text":"Projection Layer","fontSize":16},{"text":"configurable output schema","fontSize":12,"color":"gray"}],"icon":"layout-template","bgColor":"#FFF4E0","borderColor":"#E2A04A"},"compound":{"type":"parent","containerType":"freeform"},"type":"freeform","width":200,"height":100,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":1401170814,"version":1,"zIndex":21},{"strokeColor":"#1c1c1c","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","strokeSharpness":"round","opacity":100,"roughness":1,"shouldApplyRoughness":true,"isDeleted":false,"diagramId":"O1r0teKRzQDDxw1Q17ym","figureId":null,"id":"a1c685c4a9c487de40d0535f3d242cce","x":2334,"y":255,"diagramEntityId":"output","isContainer":false,"freeform":{"tag":"Shape","shape":"document","texts":[{"text":"Output JSON","fontSize":16},{"text":"final validated file","fontSize":12,"color":"gray"}],"icon":"file-json","bgColor":"#E8FDEC","borderColor":"#4AB562"},"compound":{"type":"parent","containerType":"freeform"},"type":"freeform","width":200,"height":100,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":918868834,"version":1,"zIndex":23},{"id":"d45976f0a765bde3df9182d15bd39170","type":"arrow","x":260,"y":300,"points":[[0,0],[30,0],[30,5],[60,5]],"diagramId":"O1r0teKRzQDDxw1Q17ym","diagramEntityId":"r1","backgroundColor":"transparent","fillStyle":"solid","strokeSharpness":"elbow","roughness":0,"opacity":100,"arrowHeadSize":12,"cardinalElbowData":{"isEnabled":true,"preferredSegmentDirections":["right","down","right"]},"freeform":{"tag":"Relationship","from":"g_inputs","to":"extractors"},"strokeColor":"#1c1c1c","strokeWidth":0.75,"strokeStyle":"solid","startArrowhead":null,"endArrowhead":"triangle","lastCommittedPoint":null,"startBinding":{"elementId":"d37c9b44c9b9fe1827d03f5a62beaaab","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"right"}},"endBinding":{"elementId":"5447d1bac1d338838bb67331a38bb20a","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"left"}},"width":60,"height":5,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":1275668094,"version":4,"isDeleted":false,"compound":{"type":"parent","containerType":"freeform-relationship"},"zIndex":8,"modifiedAt":1782853111413},{"id":"cab9fd39f4f1f5bc48b42461c5c8ae55","type":"arrow","x":503,"y":305,"points":[[0,0],[60,0]],"diagramId":"O1r0teKRzQDDxw1Q17ym","diagramEntityId":"r6","backgroundColor":"transparent","fillStyle":"solid","strokeSharpness":"elbow","roughness":0,"opacity":100,"arrowHeadSize":12,"cardinalElbowData":{"isEnabled":true,"preferredSegmentDirections":["right"]},"freeform":{"tag":"Relationship","from":"extractors","fromPort":"right","to":"intermediate","toPort":"left"},"strokeColor":"#1c1c1c","strokeWidth":0.75,"strokeStyle":"solid","startArrowhead":null,"endArrowhead":"triangle","lastCommittedPoint":null,"startBinding":{"elementId":"5447d1bac1d338838bb67331a38bb20a","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"right"}},"endBinding":{"elementId":"a0af5be08cd21090dd4c98d645b42352","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"left"}},"width":60,"height":0,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":828442722,"version":4,"isDeleted":false,"compound":{"type":"parent","containerType":"freeform-relationship"},"zIndex":10,"modifiedAt":1782853111413},{"id":"2f7233e168de72f66f335a230df2c603","type":"arrow","x":753,"y":305,"points":[[0,0],[60,0]],"diagramId":"O1r0teKRzQDDxw1Q17ym","diagramEntityId":"r7","backgroundColor":"transparent","fillStyle":"solid","strokeSharpness":"elbow","roughness":0,"opacity":100,"arrowHeadSize":12,"cardinalElbowData":{"isEnabled":true,"preferredSegmentDirections":["right"]},"freeform":{"tag":"Relationship","from":"intermediate","fromPort":"right","to":"normalize","toPort":"left"},"strokeColor":"#1c1c1c","strokeWidth":0.75,"strokeStyle":"solid","startArrowhead":null,"endArrowhead":"triangle","lastCommittedPoint":null,"startBinding":{"elementId":"a0af5be08cd21090dd4c98d645b42352","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"right"}},"endBinding":{"elementId":"1e61449f2f81af4711d2aa00f1eed77d","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"left"}},"width":60,"height":0,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":1465624254,"version":4,"isDeleted":false,"compound":{"type":"parent","containerType":"freeform-relationship"},"zIndex":12,"modifiedAt":1782853111413},{"id":"ee30faa5036af29f88f0b14c0c9644ba","type":"arrow","x":993,"y":305,"points":[[0,0],[60,0]],"diagramId":"O1r0teKRzQDDxw1Q17ym","diagramEntityId":"r8","backgroundColor":"transparent","fillStyle":"solid","strokeSharpness":"elbow","roughness":0,"opacity":100,"arrowHeadSize":12,"cardinalElbowData":{"isEnabled":true,"preferredSegmentDirections":["right"]},"freeform":{"tag":"Relationship","from":"normalize","fromPort":"right","to":"canonical","toPort":"left"},"strokeColor":"#1c1c1c","strokeWidth":0.75,"strokeStyle":"solid","startArrowhead":null,"endArrowhead":"triangle","lastCommittedPoint":null,"startBinding":{"elementId":"1e61449f2f81af4711d2aa00f1eed77d","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"right"}},"endBinding":{"elementId":"1adb42fe3eb967c7cf5eb3bee6f85cff","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"left"}},"width":60,"height":0,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":447065122,"version":4,"isDeleted":false,"compound":{"type":"parent","containerType":"freeform-relationship"},"zIndex":14,"modifiedAt":1782853111413},{"id":"0c739f9f69e8807b9c021f7957103a3c","type":"arrow","x":1243,"y":305,"points":[[0,0],[60,0]],"diagramId":"O1r0teKRzQDDxw1Q17ym","diagramEntityId":"r9","backgroundColor":"transparent","fillStyle":"solid","strokeSharpness":"elbow","roughness":0,"opacity":100,"arrowHeadSize":12,"cardinalElbowData":{"isEnabled":true,"preferredSegmentDirections":["right"]},"freeform":{"tag":"Relationship","from":"canonical","fromPort":"right","to":"validation","toPort":"left"},"strokeColor":"#1c1c1c","strokeWidth":0.75,"strokeStyle":"solid","startArrowhead":null,"endArrowhead":"triangle","lastCommittedPoint":null,"startBinding":{"elementId":"1adb42fe3eb967c7cf5eb3bee6f85cff","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"right"}},"endBinding":{"elementId":"7903a74e9b083e1f71631905da7b7a74","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"left"}},"width":60,"height":0,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":217325310,"version":4,"isDeleted":false,"compound":{"type":"parent","containerType":"freeform-relationship"},"zIndex":16,"modifiedAt":1782853111413},{"id":"a294f6c312301b985e37e06ab6e922c5","type":"arrow","x":1494,"y":305,"points":[[0,0],[60,0]],"diagramId":"O1r0teKRzQDDxw1Q17ym","diagramEntityId":"r10","backgroundColor":"transparent","fillStyle":"solid","strokeSharpness":"elbow","roughness":0,"opacity":100,"arrowHeadSize":12,"cardinalElbowData":{"isEnabled":true,"preferredSegmentDirections":["right"]},"freeform":{"tag":"Relationship","from":"validation","fromPort":"right","to":"merge","toPort":"left"},"strokeColor":"#1c1c1c","strokeWidth":0.75,"strokeStyle":"solid","startArrowhead":null,"endArrowhead":"triangle","lastCommittedPoint":null,"startBinding":{"elementId":"7903a74e9b083e1f71631905da7b7a74","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"right"}},"endBinding":{"elementId":"adce85252544e261102fb9c1ba660342","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"left"}},"width":60,"height":0,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":52418530,"version":4,"isDeleted":false,"compound":{"type":"parent","containerType":"freeform-relationship"},"zIndex":18,"modifiedAt":1782853111413},{"id":"b7e7cc727bef932c8c0f038ae2b0a507","type":"arrow","x":1754,"y":305,"points":[[0,0],[60,0]],"diagramId":"O1r0teKRzQDDxw1Q17ym","diagramEntityId":"r11","backgroundColor":"transparent","fillStyle":"solid","strokeSharpness":"elbow","roughness":0,"opacity":100,"arrowHeadSize":12,"cardinalElbowData":{"isEnabled":true,"preferredSegmentDirections":["right"]},"freeform":{"tag":"Relationship","from":"merge","fromPort":"right","to":"confidence","toPort":"left"},"strokeColor":"#1c1c1c","strokeWidth":0.75,"strokeStyle":"solid","startArrowhead":null,"endArrowhead":"triangle","lastCommittedPoint":null,"startBinding":{"elementId":"adce85252544e261102fb9c1ba660342","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"right"}},"endBinding":{"elementId":"39be32a95b8598f259f26ec919508766","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"left"}},"width":60,"height":0,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":559124286,"version":4,"isDeleted":false,"compound":{"type":"parent","containerType":"freeform-relationship"},"zIndex":20,"modifiedAt":1782853111413},{"id":"453ccd86953eb62bafbbf373adf38404","type":"arrow","x":2014,"y":305,"points":[[0,0],[60,0]],"diagramId":"O1r0teKRzQDDxw1Q17ym","diagramEntityId":"r12","backgroundColor":"transparent","fillStyle":"solid","strokeSharpness":"elbow","roughness":0,"opacity":100,"arrowHeadSize":12,"cardinalElbowData":{"isEnabled":true,"preferredSegmentDirections":["right"]},"freeform":{"tag":"Relationship","from":"confidence","fromPort":"right","to":"projection","toPort":"left"},"strokeColor":"#1c1c1c","strokeWidth":0.75,"strokeStyle":"solid","startArrowhead":null,"endArrowhead":"triangle","lastCommittedPoint":null,"startBinding":{"elementId":"39be32a95b8598f259f26ec919508766","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"right"}},"endBinding":{"elementId":"818c0070d4da9fc5d1be43aff9cadd01","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"left"}},"width":60,"height":0,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":2061405090,"version":4,"isDeleted":false,"compound":{"type":"parent","containerType":"freeform-relationship"},"zIndex":22,"modifiedAt":1782853111413},{"id":"106cc65f03191aadcf9e24abf4a0411c","type":"arrow","x":2274,"y":305,"points":[[0,0],[60,0]],"diagramId":"O1r0teKRzQDDxw1Q17ym","diagramEntityId":"r13","backgroundColor":"transparent","fillStyle":"solid","strokeSharpness":"elbow","roughness":0,"opacity":100,"arrowHeadSize":12,"cardinalElbowData":{"isEnabled":true,"preferredSegmentDirections":["right"]},"freeform":{"tag":"Relationship","from":"projection","fromPort":"right","to":"output","toPort":"left"},"strokeColor":"#1c1c1c","strokeWidth":0.75,"strokeStyle":"solid","startArrowhead":null,"endArrowhead":"triangle","lastCommittedPoint":null,"startBinding":{"elementId":"818c0070d4da9fc5d1be43aff9cadd01","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"right"}},"endBinding":{"elementId":"a1c685c4a9c487de40d0535f3d242cce","bindingType":"portOrCenter","portLocationOptions":{"portLocation":"varying.CardinalDirection","preferredDirection":"left"}},"width":60,"height":0,"angle":0,"groupIds":[],"lockedGroupId":null,"seed":282785662,"version":4,"isDeleted":false,"compound":{"type":"parent","containerType":"freeform-relationship"},"zIndex":24,"modifiedAt":1782853111413}],"diagramMetadata":{"settings":{},"diagramType":"freeform-diagram","diagramId":"O1r0teKRzQDDxw1Q17ym","entitySettings":{}}}

Each stage has a single responsibility, which keeps extraction, normalization, merging, and output formatting independently testable and swappable.

---

## Project Structure

```
candidate-transformer/
│
├── config/
│   └── default.json
│
├── sample_data/
│   ├── structured/
│   └── unstructured/
│
├── outputs/
│
├── src/
│   ├── extractors/
│   ├── merge/
│   ├── models/
│   ├── normalizers/
│   ├── projection/
│   ├── validation/
│   ├── utils/
│   └── pipeline.py
│
├── tests/
│
├── requirements.txt
├── design.pdf
└── README.md
```

---

## Source Priority

When the same field appears in multiple sources, the merge resolver picks a value using this priority order (configurable in `config/default.json`):

| Priority | Source         |
|----------|----------------|
| 1        | Recruiter CSV  |
| 2        | ATS JSON       |
| 3        | LinkedIn       |
| 4        | GitHub         |
| 5        | Resume PDF     |
| 6        | Resume TXT     |

---

## Technologies Used

| Library          | Purpose                          |
|-------------------|-----------------------------------|
| `pydantic`        | Data modeling & validation       |
| `rapidfuzz`       | Fuzzy matching for deduplication |
| `phonenumbers`    | Phone number parsing/E.164       |
| `python-dateutil` | Flexible date parsing            |
| `pycountry`       | Country code normalization       |
| `pytest`          | Testing framework                |


Compatible with **Python 3.11+** (tested with Python 3.13).

---

## Installation

```bash
git clone https://github.com/Disswain/candidate-transformer.git
cd candidate-transformer

python -m venv .venv
```

**Windows**

```powershell
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

## CLI Help

Display all available command-line options:

```bash
python -m src.main --help
```

Example output:

```
usage: candidate-transformer [-h]
                             --input INPUT
                             --config CONFIG
                             --output OUTPUT

options:
  -h, --help         show this help message and exit
  --input INPUT      Directory containing input candidate files
  --config CONFIG    Path to configuration JSON
  --output OUTPUT    Output JSON file path
```

```bash
python -m src.main --input sample_data --config config/default.json --output outputs/result.json
```

| Flag       | Description                                  |
|------------|-----------------------------------------------|
| `--input`  | Directory containing source candidate files   |
| `--config` | Path to pipeline configuration JSON           |
| `--output` | Destination path for the canonical output JSON|

---

## Running Tests

```bash
pytest
```

```
==========================
8 passed in 2.7s
==========================
```

The project contains automated unit tests covering:

- Phone normalization
- Email normalization
- Name normalization
- Skill normalization
- Date normalization
- Merge resolver
- Projection layer
- End-to-end pipeline execution

---

## Sample Output

```json
{
  "candidate_id": "C001",
  "full_name": "John Anderson",
  "emails": [
    "john.anderson@example.com"
  ],
  "phones": [
    "+14155551234"
  ],
  "location": {
    "city": "San Francisco",
    "region": "California",
    "country": "US"
  }
}
```

The generated output also includes normalized skills, experience, education, confidence scores, and field-level provenance.

---

## Configuration

All transformation behavior is driven by `config/default.json`, including:

- Source priority order
- Confidence weight tuning per source/field
- Which fields appear in the final projected output
- Behavior when a field is missing across all sources
- Normalization rules (e.g. date formats, phone region defaults)

---

## Design Decisions

- **Intermediate data model** isolates raw extraction from normalization logic.
- **Single-responsibility normalizers** — one normalizer, one concern (e.g. just phone numbers).
- **Merge logic is decoupled from extraction**, so new sources don't require touching the resolver.
- **Configurable projection layer** lets consumers request only the fields they need.
- **Confidence and provenance are computed post-merge**, once the final value per field is known.
- **Modular architecture** — new extractors or normalizers can be added with minimal changes elsewhere.

---

## Assumptions

- All input files in a given run belong to the same candidate.
- Recruiter CSV is treated as the most reliable source.
- Phone numbers are normalized to E.164 format.
- Countries are normalized to ISO-3166 Alpha-2 codes.
- Duplicate skills are merged case-insensitively.
- Invalid emails and phone numbers are dropped rather than blocking the pipeline.

---

## Future Improvements

- [ ] OCR support for scanned resumes
- [ ] Entity resolution across multiple candidates
- [ ] Machine learning–based confidence scoring
- [ ] REST API interface
- [ ] Database persistence layer
- [ ] Parallelized extraction pipeline

---

## Author

**Disita Swain**
B.Tech Computer Science & Engineering (Cybersecurity)
SOA University
