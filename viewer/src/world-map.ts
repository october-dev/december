export type TileLayer = number[][];

export type WorldMap = {
  width: number;
  height: number;
  tileSetUrl: string;
  tileSetDimX: number;
  tileSetDimY: number;
  tileDim: number;
  bgTiles: TileLayer[];
  objectTiles: TileLayer[];
  animatedSprites: never[];
};
