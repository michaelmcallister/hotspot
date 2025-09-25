export function riskToSafetyScore(riskScore: number): number {
  return Math.round((1 - riskScore) * 100);
}

export function safetyToRiskScore(safetyScore: number): number {
  return 1 - (safetyScore / 100);
}

export function riskDifferencePercent(suburbRisk: number, averageRisk: number): number {
  return ((suburbRisk - averageRisk) / averageRisk) * 100;
}