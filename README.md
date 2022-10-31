# Foggy

This is a hobby/fun/exploratory project aiming to forecast fog creation on various places. The motivation is to recognize good conditions
for landscape photography :-)

It uses [Yr.no](https://docs.api.met.no/doc/locationforecast/HowTO) data as they are well-known and well-trusted, detailed and free.

## Project phases

The project has/will have several phases:

### PoC v1

I'm trying to assemble some working algorithm for forecasting the fog. It will be verified manually, using a single location and a webcam
placed nearby.

### PoC v2

_in case PoC v1 will be considered successful_

This will improve PoC v1 by automatic analysis of the result. That will be done (probably) by some AI-based analysis of the webcam shots.

### MVP

API will be implemented, documentation written and the whole service deployed somewhere to be publicly available.

## Current state

Current status is that I'm moving this project to [PoC v2](#poc-v2).

## Current/possible future features

Features that this project _could_ possibly implement:

- [x] Being able to forecast fog for a single place - wind speed, relative humidity, dew point
- [x] Being able to forecast fog for various places
- [ ] Provide public API for forecasts
- [ ] Water coefficient: detect amount of water (ponds, lakes, rivers) near the place and convert to the coefficient
- [ ] Terrain coefficient: detect valleys etc.
- [ ] Throw this whole thing away and use some AI instead - using similarities to historic data maybe?
