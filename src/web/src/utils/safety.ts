export function safetyLabel(score: number): string {
  if (score >= 80) return 'Low Risk'
  if (score >= 50) return 'Medium Risk'
  return 'High Risk'
}

export function safetyColour(score: number): string {
  if (score >= 80) return 'success'
  if (score >= 50) return 'warning'
  return 'error'
}

