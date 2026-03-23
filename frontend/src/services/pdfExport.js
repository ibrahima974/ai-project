import jsPDF from 'jspdf'

export function exportInsightToPDF(insight) {
  const doc    = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' })
  const pageW  = doc.internal.pageSize.getWidth()
  const pageH  = doc.internal.pageSize.getHeight()
  const margin = 20
  const maxW   = pageW - margin * 2
  let   y      = margin

  const categoryColors = {
    Sales:     [59,  130, 246],
    Marketing: [16,  185, 129],
    Support:   [245, 158, 11]
  }
  const color = categoryColors[insight.category] || [99, 102, 241]

  // ── Header band ──────────────────────────────────────────────────
  doc.setFillColor(...color)
  doc.rect(0, 0, pageW, 40, 'F')

  doc.setTextColor(255, 255, 255)
  doc.setFontSize(20)
  doc.setFont('helvetica', 'bold')
  doc.text('InsightIQ', margin, 16)

  doc.setFontSize(10)
  doc.setFont('helvetica', 'normal')
  doc.text('AI-Powered Analytics Dashboard', margin, 24)

  // Badge catégorie
  doc.setFillColor(255, 255, 255, 0.25)
  doc.roundedRect(pageW - margin - 30, 10, 30, 10, 3, 3, 'F')
  doc.setTextColor(255, 255, 255)
  doc.setFontSize(9)
  doc.setFont('helvetica', 'bold')
  doc.text(insight.category.toUpperCase(), pageW - margin - 15, 16.5, { align: 'center' })

  y = 52

  // ── Titre ────────────────────────────────────────────────────────
  doc.setTextColor(17, 24, 39)
  doc.setFontSize(16)
  doc.setFont('helvetica', 'bold')
  const titleLines = doc.splitTextToSize(insight.title, maxW)
  doc.text(titleLines, margin, y)
  y += titleLines.length * 8 + 4

  // Date
  doc.setFontSize(9)
  doc.setFont('helvetica', 'normal')
  doc.setTextColor(156, 163, 175)
  const dateStr = new Date(insight.generated_at).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
  doc.text(`Généré le ${dateStr}`, margin, y)
  y += 6

  // Ligne séparatrice
  doc.setDrawColor(...color)
  doc.setLineWidth(0.5)
  doc.line(margin, y, pageW - margin, y)
  y += 8

  // ── Contenu ───────────────────────────────────────────────────────
  const lines = insight.content.split('\n')

  for (const line of lines) {
    if (y > pageH - margin - 20) {
      doc.addPage()
      y = margin
    }

    const trimmed = line.trim()

    if (trimmed.startsWith('## ')) {
      // Titre de section
      y += 4
      const sectionTitle = trimmed.replace('## ', '')

      doc.setFillColor(...color.map(c => Math.min(255, c + 180)))
      doc.roundedRect(margin - 2, y - 5, maxW + 4, 10, 2, 2, 'F')

      doc.setFontSize(11)
      doc.setFont('helvetica', 'bold')
      doc.setTextColor(...color)
      doc.text(sectionTitle, margin, y + 1)
      y += 10

    } else if (trimmed === '') {
      y += 3

    } else {
      doc.setFontSize(10)
      doc.setFont('helvetica', 'normal')
      doc.setTextColor(55, 65, 81)

      const wrapped = doc.splitTextToSize(trimmed, maxW - 4)
      for (const wline of wrapped) {
        if (y > pageH - margin - 10) {
          doc.addPage()
          y = margin
        }
        doc.text(wline, margin + 2, y)
        y += 6
      }
    }
  }

  // ── Footer ────────────────────────────────────────────────────────
  const totalPages = doc.internal.getNumberOfPages()
  for (let i = 1; i <= totalPages; i++) {
    doc.setPage(i)
    doc.setFillColor(249, 250, 251)
    doc.rect(0, pageH - 12, pageW, 12, 'F')
    doc.setFontSize(8)
    doc.setTextColor(156, 163, 175)
    doc.setFont('helvetica', 'normal')
    doc.text('InsightIQ — Rapport généré par Claude AI', margin, pageH - 5)
    doc.text(`Page ${i} / ${totalPages}`, pageW - margin, pageH - 5, { align: 'right' })
  }

  // ── Téléchargement ────────────────────────────────────────────────
  const filename = `InsightIQ_${insight.category}_${new Date(insight.generated_at)
    .toISOString().slice(0, 10)}.pdf`
  doc.save(filename)
}