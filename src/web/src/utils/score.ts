export const riskToSafetyScore = (riskScore: number): number => Math.round((1 - riskScore) * 100)

export const safetyToRiskScore = (safetyScore: number): number => 1 - safetyScore / 100

export const riskDifferencePercent = (
  suburbRisk: number,
  averageRisk: number
): number => ((suburbRisk - averageRisk) / averageRisk) * 100
