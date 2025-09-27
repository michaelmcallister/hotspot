export const safetyLabel = (score: number): string => {
  if (score >= 80) return 'Low Risk';
  if (score >= 50) return 'Medium Risk';
  return 'High Risk';
}

export const safetyColor = (score: number): string => {
  if (score >= 80) return 'success';
  if (score >= 50) return 'warning';
  return 'error';
}
