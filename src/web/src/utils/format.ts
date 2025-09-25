export function formatDistance(meters: number): string {
  if (meters < 1000) {
    return `${Math.round(meters)}m`;
  } else {
    return `${(meters / 1000).toFixed(1)}km`;
  }
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-AU', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
}

export function formatParkingType(type: string): string {
  const types: Record<string, string> = {
    'on-street': 'On Street',
    'off-street': 'Off Street',
    'secure': 'Secure'
  };
  return types[type] || type;
}

export function getLightingLabel(rating: number): string {
  const labels: Record<number, string> = {
    1: 'Poor',
    2: 'Fair',
    3: 'Good',
    4: 'Excellent'
  };
  return labels[rating] || 'Unknown';
}