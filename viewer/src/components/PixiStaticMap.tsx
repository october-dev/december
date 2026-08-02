import { PixiComponent, applyDefaultProps } from '@pixi/react';
import * as PIXI from 'pixi.js';
import type { WorldMap } from '../world-map';

export const PixiStaticMap = PixiComponent('StaticMap', {
  create: (props: { map: WorldMap; [key: string]: unknown }) => {
    const { map } = props;
    const columns = Math.floor(map.tileSetDimX / map.tileDim);
    const rows = Math.floor(map.tileSetDimY / map.tileDim);
    const baseTexture = PIXI.BaseTexture.from(map.tileSetUrl, {
      scaleMode: PIXI.SCALE_MODES.NEAREST,
    });
    const tiles: PIXI.Texture[] = [];
    for (let x = 0; x < columns; x += 1) {
      for (let y = 0; y < rows; y += 1) {
        tiles[x + y * columns] = new PIXI.Texture(
          baseTexture,
          new PIXI.Rectangle(x * map.tileDim, y * map.tileDim, map.tileDim, map.tileDim),
        );
      }
    }

    const screenColumns = map.bgTiles[0].length;
    const screenRows = map.bgTiles[0][0].length;
    const container = new PIXI.Container();
    for (let index = 0; index < screenColumns * screenRows; index += 1) {
      const x = index % screenColumns;
      const y = Math.floor(index / screenColumns);
      for (const layer of [...map.bgTiles, ...map.objectTiles]) {
        const tileIndex = layer[x][y];
        if (tileIndex === -1) continue;
        const sprite = new PIXI.Sprite(tiles[tileIndex]);
        sprite.x = x * map.tileDim;
        sprite.y = y * map.tileDim;
        container.addChild(sprite);
      }
    }
    container.interactive = true;
    container.hitArea = new PIXI.Rectangle(
      0,
      0,
      screenColumns * map.tileDim,
      screenRows * map.tileDim,
    );
    return container;
  },
  applyProps: (instance, oldProps, newProps) => applyDefaultProps(instance, oldProps, newProps),
});
