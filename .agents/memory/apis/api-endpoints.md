# API Memory: Presentation REST Endpoints

## Base Path: `/api/v1`

| Method | Path | Description | Request Schema | Response Schema |
|--------|------|-------------|----------------|-----------------|
| `POST` | `/api/v1/calculate` | Compute ability and spell cooldowns | `CalculateRequestSchema` | `CalculateResponseSchema` |
| `GET`  | `/api/v1/champions` | List all champions | None | `list[ChampionResponseSchema]` |
| `GET`  | `/api/v1/champions/{id}` | Get champion with abilities | None | `ChampionResponseSchema` |
| `GET`  | `/api/v1/items` | List items with search filter | `search: str` (query) | `list[ItemResponseSchema]` |
| `GET`  | `/api/v1/runes` | List haste-affecting runes | None | `list[RuneResponseSchema]` |
| `GET`  | `/api/v1/summoner-spells` | List summoner spells | None | `list[SpellResponseSchema]` |
| `POST` | `/api/v1/sync` | Ingest patch data from Data Dragon | `force: bool` (query) | `dict` |
| `GET`  | `/api/v1/health` | Service health check | None | `{"status": "ok"}` |

## Schema Notes
- `CalculateResponseSchema`: Exposes `ability_haste`, `ultimate_haste`, `summoner_haste`, and `basic_haste` alongside per-ability cooldown breakdowns.
- `ItemResponseSchema`: Includes `ability_haste`, `ultimate_haste`, `basic_haste`, and `summoner_haste`.
