// 读家里发来的 PDF（练习题、词表扫描件）：每页导出 PNG 和文字，没有文字层时用 macOS 自带 OCR。
// 编译：swiftc -O tools/pdftext.swift -o /tmp/pdftext；用法：/tmp/pdftext <pdf> <输出文件夹>（文件夹要先建好）
import PDFKit
import Vision
import AppKit
// usage: pdftext <pdf> <outdir>  — writes page text (text layer, or OCR when a page has none) and page PNGs
let args = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: args[1]))!
let out = args[2]
for i in 0..<doc.pageCount {
    let page = doc.page(at: i)!
    var text = page.string ?? ""
    let box = page.bounds(for: .mediaBox)
    let scale: CGFloat = 2
    let img = NSImage(size: NSSize(width: box.width * scale, height: box.height * scale))
    img.lockFocus()
    NSColor.white.set(); NSRect(origin: .zero, size: img.size).fill()
    let ctx = NSGraphicsContext.current!.cgContext
    ctx.scaleBy(x: scale, y: scale)
    page.draw(with: .mediaBox, to: ctx)
    img.unlockFocus()
    let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
    let png = rep.representation(using: .png, properties: [:])!
    try! png.write(to: URL(fileURLWithPath: "\(out)/p\(i + 1).png"))
    if text.trimmingCharacters(in: .whitespacesAndNewlines).count < 40 {
        let req = VNRecognizeTextRequest()
        req.recognitionLevel = .accurate
        req.recognitionLanguages = ["en-US"]
        try! VNImageRequestHandler(cgImage: rep.cgImage!, options: [:]).perform([req])
        text = "[OCR]\n" + (req.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
    }
    try! text.write(toFile: "\(out)/p\(i + 1).txt", atomically: true, encoding: .utf8)
}
print(doc.pageCount)
