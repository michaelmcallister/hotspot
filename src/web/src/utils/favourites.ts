const FAVOURITES_KEY = 'parkingFavourites';
const CACHE_KEY = 'parkingDataCache';

export const getFavouriteIds = (): number[] => {
  try {
    const stored = localStorage.getItem(FAVOURITES_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch (error) {
    console.error('Error reading favourites from localStorage:', error);
    return [];
  }
}

export const isFavourite = (parkingId: number): boolean => {
  const favourites = getFavouriteIds();
  return favourites.includes(parkingId);
}

export const addToFavourites = (parkingId: number): void => {
  const favourites = getFavouriteIds();
  if (!favourites.includes(parkingId)) {
    favourites.push(parkingId);
    saveFavourites(favourites);
  }
}

export const removeFromFavourites = (parkingId: number): void => {
  const favourites = getFavouriteIds();
  const filtered = favourites.filter((id) => id !== parkingId);
  saveFavourites(filtered);
}

export const toggleFavourite = (parkingId: number): boolean => {
  const isCurrentlyFavourite = isFavourite(parkingId);
  if (isCurrentlyFavourite) {
    removeFromFavourites(parkingId);
  } else {
    addToFavourites(parkingId);
  }
  return !isCurrentlyFavourite;
}

const saveFavourites = (favourites: number[]): void => {
  try {
    localStorage.setItem(FAVOURITES_KEY, JSON.stringify(favourites));
  } catch (error) {
    console.error('Error saving favourites to localStorage:', error);
  }
}

interface CachedParkingData {
  parking_id: number;
  address: string;
  suburb: string;
  postcode: string;
  type: string;
  lighting: number | null;
  cctv: boolean | null;
  created_at: string;
  facilities: Array<{
    facility_id: number;
    facility_name: string;
  }>;
}

export const getCachedParkingData = (): Record<number, CachedParkingData> => {
  try {
    const stored = localStorage.getItem(CACHE_KEY);
    return stored ? JSON.parse(stored) : {};
  } catch (error) {
    console.error('Error reading cached parking data:', error);
    return {};
  }
}

export const setCachedParkingData = (data: Record<number, CachedParkingData>): void => {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify(data));
  } catch (error) {
    console.error('Error saving cached parking data:', error);
  }
}

export const clearAllFavouriteData = (): void => {
  try {
    localStorage.removeItem(FAVOURITES_KEY);
    localStorage.removeItem(CACHE_KEY);
  } catch (error) {
    console.error('Error clearing favourite data:', error);
  }
}
