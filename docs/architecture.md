# Project Architecture

This document describes the executable architecture of this project based on `main.py`.

## 1) Module Dependency Graph

```mermaid
flowchart TD
    subgraph "Application Module"
        M["main.py"]
    end

    subgraph "Third-Party Library"
        P["pygame"]
    end

    subgraph "Python Standard Library"
        R["random"]
        D["dataclasses.dataclass"]
        S["math.sqrt"]
    end

    M --> P
    M --> R
    M --> D
    M --> S
```

Notes:
- The codebase currently has one executable Python module (`main.py`).
- All runtime behavior is orchestrated from `main()`.

## 2) High-Level Runtime Flow Graph

```mermaid
flowchart TD
    A["Program Start"] --> B["Call main()"]
    B --> C["Initialize pygame systems"]
    C --> D["Create window and clock"]
    D --> E["Create initial list of squares"]
    E --> F["Enter frame loop (while running)"]

    F --> G["Read pygame events"]
    G --> H["Process each event via handle_input()"]
    H --> I{"Quit requested?"}
    I -->|"Yes"| J["Set running = False"]
    I -->|"No"| K["Continue frame"]

    K --> L["Fill background"]
    L --> M{"Paused?"}
    M -->|"No"| N["Update each square via update_square()"]
    M -->|"Yes"| O["Skip square updates"]

    N --> P["Draw each square"]
    O --> P
    P --> Q["Draw overlay text"]
    Q --> R["Flip display"]
    R --> S["Tick clock at target FPS"]
    S --> F

    J --> T["Quit pygame"]
    T --> U["Program End"]
```

## 3) Function-Level Call Graph

```mermaid
flowchart TD
    M0["main()"] --> M1["pygame.init()"]
    M0 --> M2["pygame.display.set_mode()"]
    M0 --> M3["pygame.display.set_caption()"]
    M0 --> M4["pygame.time.Clock()"]
    M0 --> M5["create_random_square()"]
    M0 --> M6["pygame.event.get()"]
    M0 --> M7["handle_input(event, paused, target_fps, squares)"]
    M0 --> M8["update_square(square, squares)"]
    M0 --> M9["draw_square(screen, square)"]
    M0 --> M10["draw_overlay(screen, paused, target_fps)"]
    M0 --> M11["pygame.display.flip()"]
    M0 --> M12["clock.tick(target_fps)"]
    M0 --> M13["pygame.quit()"]

    M5 --> C1["get_color_for_size(size)"]

    M7 --> H1["create_random_square() (on reset key)"]

    M8 --> U1["create_random_square() (on lifespan expiry)"]
    M8 --> U2["apply_flee_behavior(square, all_squares)"]
    M8 --> U3["apply_chase_behavior(square, all_squares)"]

    U2 --> F1["math.sqrt()"]
    U3 --> F2["math.sqrt()"]
```

## 4) Primary Execution Sequence Diagram

```mermaid
sequenceDiagram
    participant User as "User"
    participant Pygame as "Pygame Event System"
    participant Main as "main() Loop"
    participant Input as "handle_input()"
    participant Update as "update_square()"
    participant Flee as "apply_flee_behavior()"
    participant Chase as "apply_chase_behavior()"
    participant Draw as "draw_square() / draw_overlay()"
    participant RNG as "create_random_square()"

    Main->>Pygame: "Initialize runtime and window"
    Main->>RNG: "Create initial SQUARE_COUNT squares"

    loop "Each Frame While Running"
        Main->>Pygame: "Get events"
        loop "For Each Event"
            Main->>Input: "handle_input(event, paused, target_fps, squares)"
            alt "Quit Event or ESC"
                Input-->>Main: "should_quit = True"
                Main-->>Main: "running = False"
            else "SPACE Pressed"
                Input-->>Main: "toggle paused"
            else "R Pressed"
                Input->>RNG: "Rebuild square list"
                Input-->>Main: "updated squares"
            else "Other Event"
                Input-->>Main: "no state change"
            end
        end

        Main-->>Main: "Fill background"

        alt "paused == False"
            loop "For Each Square"
                Main->>Update: "update_square(square, all_squares)"
                Update-->>Update: "Increment age"
                alt "age >= lifespan"
                    Update->>RNG: "Replace with new random square"
                    RNG-->>Update: "new Square"
                else "age < lifespan"
                    Update->>Flee: "Apply flee vector from larger neighbors"
                    Flee-->>Update: "Adjusted velocity"
                    Update->>Chase: "Apply chase vector toward smaller neighbors"
                    Chase-->>Update: "Adjusted velocity"
                    Update-->>Update: "Advance position and bounce on bounds"
                end
                Main->>Draw: "Draw square"
            end
        else "paused == True"
            Main-->>Main: "Skip update_square calls"
            loop "For Each Square"
                Main->>Draw: "Draw square"
            end
        end

        Main->>Draw: "Draw status overlay"
        Main->>Pygame: "Flip display and tick clock"
    end

    Main->>Pygame: "Quit runtime"
```

## Architecture Notes

- The architecture is intentionally centralized: one module controls initialization, event handling, simulation updates, and rendering.
- Simulation state is mutable and frame-based, with in-place square updates except when lifespan expiry triggers object replacement.
- Behavior composition inside `update_square()` combines local movement, flee response, chase response, and boundary constraints in a deterministic order.

## Assumptions

- The documented primary path assumes normal execution from `python main.py` with no runtime import errors.
- `find_nearest()` exists in code but is currently not called by the active execution path.
