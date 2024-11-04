generated with mermaid.js cli tool
mmdc -i database-schema.md -o database-schema.png -t dark

if commands fails try with this
[script](https://github.com/YoAquinJs/bash-env/blob/main/bin/mmdc-compile)

```bash

mmdc-compile database-schema.md -t dark
```

Game status are: pending, draw, black won, white won

```mermaid
erDiagram
    Board_Client {
        string token
    }
    User {
        string name
        password pw
    }
    Chess_Game {
        User white_user
        User black_user
        int status
    }
    Chess_Movement {
        int index
        int16 encoded_movement
    }

    User ||--o| Board_Client : Registers

    User ||--o{ Chess_Game : Plays
    Chess_Game ||--o{ Chess_Movement : Contains
```
