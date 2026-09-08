# Project Summary: League of Legends Cooldown Calculator

## Overview
A web-based League of Legends Cooldown Calculator that computes ability and summoner spell cooldowns based on champion skills, ability ranks, items, runes, and summoner spells for the current game patch.

## Tech Stack
- **Frontend**: Vue 3 + TailwindCSS (Vite build tool)
- **Backend**: Python 3.13 / FastAPI
- **Database**: PostgreSQL
- **Primary Data Source**: Riot Data Dragon (and CommunityDragon for extended metadata when required)

## Key Constraints & Philosophy
- Simple calculation tool, not a match or combat simulator.
- Supports the current patch only (backend auto-syncs or refreshes with patch updates).
- Distinguishes Haste types: General Ability Haste, Ultimate Haste, Basic Ability Haste, Summoner Spell Haste.
- Multi-charge abilities calculate cooldown for a single charge only.
- Does not simulate complex passives (e.g., Sona Accelerando) or special stat-scaling cooldowns (e.g., Yasuo/Yone Q).
- Backend is authoritative for calculation logic via `/api/calculate`.
