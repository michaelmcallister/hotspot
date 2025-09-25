const FAVOURITES_KEY = 'parkingFavourites';
const CACHE_KEY = 'parkingDataCache';

export function getFavouriteIds(): number[] {
  try {
    const stored = localStorage.getItem(FAVOURITES_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch (error) {
    console.error('Error reading favourites from localStorage:', error);
    return [];
  }
}

export function isFavourite(parkingId: number): boolean {
  const favourites = getFavouriteIds();
  return favourites.includes(parkingId);
}

export function addToFavourites(parkingId: number): void {
  const favourites = getFavouriteIds();
  if (!favourites.includes(parkingId)) {
    favourites.push(parkingId);
    saveFavourites(favourites);
  }
}

export function removeFromFavourites(parkingId: number): void {
  const favourites = getFavouriteIds();
  const filtered = favourites.filter(id => id !== parkingId);
  saveFavourites(filtered);
}

export function toggleFavourite(parkingId: number): boolean {
  const isCurrentlyFavourite = isFavourite(parkingId);
  if (isCurrentlyFavourite) {
    removeFromFavourites(parkingId);
  } else {
    addToFavourites(parkingId);
  }
  return !isCurrentlyFavourite;
}

function saveFavourites(favourites: number[]): void {
  try {
    localStorage.setItem(FAVOURITES_KEY, JSON.stringify(favourites));
  } catch (error) {
    console.error('Error saving favourites to localStorage:', error);
  }
}

export function getCachedParkingData(): Record<number, any> {
  try {
    const stored = localStorage.getItem(CACHE_KEY);
    return stored ? JSON.parse(stored) : {};
  } catch (error) {
    console.error('Error reading cached parking data:', error);
    return {};
  }
}

export function setCachedParkingData(data: Record<number, any>): void {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify(data));
  } catch (error) {
    console.error('Error saving cached parking data:', error);
  }
}

export function clearAllFavouriteData(): void {
  try {
    localStorage.removeItem(FAVOURITES_KEY);
    localStorage.removeItem(CACHE_KEY);
  } catch (error) {
    console.error('Error clearing favourite data:', error);
  }
}