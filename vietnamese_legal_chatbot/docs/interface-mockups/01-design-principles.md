# 🎨 Design Principles & Guidelines - Part 1
# Nguyên tắc & Hướng dẫn Thiết kế - Phần 1

> **Fundamental design principles and visual guidelines for Vietnamese Legal AI Chatbot**  
> *Nguyên tắc thiết kế cơ bản và hướng dẫn thị giác cho Chatbot AI Pháp lý Việt Nam*

## 🎯 Core Design Philosophy | Triết lý Thiết kế Cốt lõi

### Vietnamese-First Design Approach | Tiếp cận Thiết kế Ưu tiên Việt Nam

```mermaid
graph TB
    subgraph "Design Pillars | Trụ cột Thiết kế"
        P1[Vietnamese Cultural Respect<br/>Tôn trọng Văn hóa Việt Nam<br/>🇻🇳]
        P2[Legal Professionalism<br/>Tính chuyên nghiệp Pháp lý<br/>⚖️]
        P3[Accessibility First<br/>Ưu tiên Khả năng tiếp cận<br/>♿]
        P4[Performance Optimized<br/>Tối ưu Hiệu suất<br/>⚡]
    end
    
    subgraph "Vietnamese UX Principles | Nguyên tắc UX Việt Nam"
        V1[Respectful Communication<br/>Giao tiếp Tôn trọng]
        V2[Hierarchical Information<br/>Thông tin Phân cấp]
        V3[Formal Tone & Language<br/>Ngôn ngữ Trang trọng]
        V4[Cultural Color Psychology<br/>Tâm lý Màu sắc Văn hóa]
    end
    
    P1 --> V1
    P2 --> V2
    P3 --> V4
    P4 --> V3
```

## 🎨 Visual Identity System | Hệ thống Nhận diện Thị giác

### Primary Color Palette | Bảng màu Chính

```mermaid
graph LR
    subgraph "Legal Professional Colors | Màu Chuyên nghiệp Pháp lý"
        C1[Primary Blue<br/>Xanh Chính<br/>#1E40AF<br/>Trust & Authority]
        C2[Deep Navy<br/>Xanh Đậm<br/>#1E3A8A<br/>Stability & Law]
        C3[Gold Accent<br/>Vàng Nhấn<br/>#F59E0B<br/>Vietnamese Heritage]
        C4[Success Green<br/>Xanh Thành công<br/>#10B981<br/>Positive Outcomes]
    end
    
    subgraph "Supporting Colors | Màu Hỗ trợ"
        S1[Light Gray<br/>Xám Nhạt<br/>#F8FAFC<br/>Background]
        S2[Medium Gray<br/>Xám Trung<br/>#64748B<br/>Secondary Text]
        S3[Warning Orange<br/>Cam Cảnh báo<br/>#F97316<br/>Important Notes]
        S4[Error Red<br/>Đỏ Lỗi<br/>#EF4444<br/>Alerts & Errors]
    end
```

### Color Usage Guidelines | Hướng dẫn Sử dụng Màu sắc

| Color | Usage | Vietnamese Context | Accessibility |
|-------|-------|-------------------|---------------|
| **#1E40AF** | Primary actions, headers | Government official blue | WCAG AA+ |
| **#1E3A8A** | Navigation, legal emphasis | Traditional Vietnamese authority | WCAG AA+ |
| **#F59E0B** | Highlights, Vietnamese elements | Golden dragon, prosperity | WCAG AA |
| **#10B981** | Success states, positive feedback | Growth, harmony | WCAG AA+ |
| **#EF4444** | Errors, critical warnings | Traditional warning red | WCAG AA |

### Typography System | Hệ thống Typography

#### Vietnamese Font Hierarchy | Phân cấp Font Tiếng Việt

```css
/* Primary Font Stack - Vietnamese Optimized */
--font-primary: 'Inter', 'Roboto', 'Noto Sans Vietnamese', 
                'SVN-Poppins', 'Arial', sans-serif;

/* Display/Header Fonts */
--font-display: 'Playfair Display', 'SVN-Gilroy', 'Georgia', serif;

/* Monospace for Code/Legal Citations */
--font-mono: 'JetBrains Mono', 'SVN-Source Code Pro', 
             'Consolas', monospace;

/* Vietnamese Specific Fonts */
--font-vietnamese: 'Noto Sans Vietnamese', 'SVN-Poppins', 
                   'Roboto Vietnamese', sans-serif;
```

#### Font Size Scale | Thang Đo Kích thước Font

```mermaid
graph TB
    subgraph "Typography Scale | Thang Typography"
        H1[H1 - Main Headers<br/>32px / 2rem<br/>Legal Document Titles]
        H2[H2 - Section Headers<br/>24px / 1.5rem<br/>Law Categories]
        H3[H3 - Subsection Headers<br/>20px / 1.25rem<br/>Article Titles]
        H4[H4 - Component Headers<br/>18px / 1.125rem<br/>FAQ Questions]
        BODY[Body Text<br/>16px / 1rem<br/>Main Content]
        SMALL[Small Text<br/>14px / 0.875rem<br/>Captions & Notes]
        TINY[Tiny Text<br/>12px / 0.75rem<br/>Legal Citations]
    end
    
    subgraph "Vietnamese Text Considerations"
        V1[Diacritics Support<br/>Hỗ trợ Dấu thanh]
        V2[Line Height 1.6<br/>Chiều cao Dòng 1.6]
        V3[Letter Spacing 0.02em<br/>Khoảng cách Chữ 0.02em]
        V4[Word Break Normal<br/>Ngắt từ Bình thường]
    end
```

### Vietnamese Typography Best Practices | Thực hành Tốt nhất Typography Việt Nam

#### 1. Diacritics & Special Characters | Dấu thanh & Ký tự Đặc biệt

```css
/* Ensure proper Vietnamese diacritics rendering */
.vietnamese-text {
    font-feature-settings: "liga" 1, "kern" 1, "calt" 1;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* Special handling for legal Vietnamese terms */
.legal-term {
    font-weight: 600;
    color: var(--color-primary);
    font-variant: small-caps;
}
```

#### 2. Line Length & Readability | Độ dài Dòng & Khả năng Đọc

```css
/* Optimal line length for Vietnamese text */
.content-text {
    max-width: 65ch; /* Optimal for Vietnamese reading */
    line-height: 1.6; /* Increased for Vietnamese diacritics */
    margin-bottom: 1.5rem;
}

/* Legal document formatting */
.legal-document {
    max-width: 70ch;
    line-height: 1.8;
    text-align: justify;
    hyphens: auto;
    hyphenate-limit-chars: 6 3 3;
}
```

## 🎭 Visual Hierarchy System | Hệ thống Phân cấp Thị giác

### Information Architecture | Kiến trúc Thông tin

```mermaid
graph TB
    subgraph "Primary Information Layer | Lớp Thông tin Chính"
        L1[Chat Interface<br/>Giao diện Chat<br/>Legal Q&A Priority]
        L2[Navigation Menu<br/>Menu Điều hướng<br/>Quick Access]
        L3[User Status<br/>Trạng thái Người dùng<br/>Authentication State]
    end
    
    subgraph "Secondary Information Layer | Lớp Thông tin Phụ"
        L4[Document Library<br/>Thư viện Tài liệu<br/>Reference Materials]
        L5[Legal Categories<br/>Danh mục Pháp lý<br/>Topic Navigation]
        L6[Recent History<br/>Lịch sử Gần đây<br/>Previous Queries]
    end
    
    subgraph "Tertiary Information Layer | Lớp Thông tin Phụ trợ"
        L7[Settings Panel<br/>Bảng Cài đặt<br/>User Preferences]
        L8[Help & Support<br/>Trợ giúp & Hỗ trợ<br/>User Guidance]
        L9[Legal Disclaimers<br/>Tuyên bố Pháp lý<br/>Compliance Info]
    end
```

### Visual Weight Distribution | Phân bố Trọng lượng Thị giác

#### Component Priority Matrix | Ma trận Ưu tiên Component

| Priority | Component | Visual Treatment | Vietnamese Consideration |
|----------|-----------|-----------------|--------------------------|
| **Critical** | Chat Input/Output | High contrast, large fonts | Proper Vietnamese input support |
| **High** | Legal Categories | Bold colors, clear icons | Vietnamese legal domain names |
| **Medium** | Navigation | Moderate emphasis | Formal Vietnamese terminology |
| **Low** | Footer/Credits | Subdued colors, small text | Professional Vietnamese tone |

## 📐 Layout & Grid System | Hệ thống Bố cục & Lưới

### Grid Framework | Khung Lưới

```css
/* Vietnamese Legal AI Chatbot Grid System */
.container {
    display: grid;
    grid-template-columns: 
        [sidebar-start] 280px 
        [content-start] 1fr 
        [aside-start] 320px [aside-end];
    grid-template-rows: 
        [header-start] 64px 
        [main-start] 1fr 
        [footer-start] 48px [footer-end];
    gap: 24px;
    min-height: 100vh;
    padding: 0 24px;
}
```

### Spacing System | Hệ thống Khoảng cách

```mermaid
graph LR
    subgraph "Spacing Scale | Thang Khoảng cách"
        S1[4px - Tight<br/>Button padding]
        S2[8px - Close<br/>Form elements]
        S3[16px - Normal<br/>Component spacing]
        S4[24px - Loose<br/>Section margins]
        S5[32px - Wide<br/>Page sections]
        S6[48px - Extra Wide<br/>Major sections]
    end
    
    subgraph "Vietnamese UI Considerations"
        V1[Increased padding for Vietnamese text]
        V2[Extra space for diacritics]
        V3[Comfortable touch targets]
        V4[Reading-friendly line spacing]
    end
```

## 🎪 Component Design Patterns | Mẫu Thiết kế Component

### Button System | Hệ thống Nút

#### Primary Buttons | Nút Chính

```css
/* Primary Action Button - Vietnamese Legal Style */
.btn-primary {
    background: linear-gradient(135deg, #1E40AF, #1E3A8A);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: 600;
    min-height: 44px; /* Touch-friendly */
    box-shadow: 0 2px 4px rgba(30, 64, 175, 0.1);
    transition: all 0.2s ease;
}

.btn-primary:hover {
    background: linear-gradient(135deg, #1E3A8A, #1E40AF);
    box-shadow: 0 4px 8px rgba(30, 64, 175, 0.2);
    transform: translateY(-1px);
}

/* Vietnamese text specific adjustments */
.btn-primary.vietnamese {
    letter-spacing: 0.02em;
    line-height: 1.4;
}
```

#### Button Hierarchy | Phân cấp Nút

```mermaid
graph TB
    subgraph "Button Types | Loại Nút"
        B1[Primary Button<br/>Nút Chính<br/>Main legal actions]
        B2[Secondary Button<br/>Nút Phụ<br/>Supporting actions]
        B3[Tertiary Button<br/>Nút Phụ trợ<br/>Minor actions]
        B4[Danger Button<br/>Nút Nguy hiểm<br/>Delete/Warning actions]
    end
    
    subgraph "Vietnamese Button Labels | Nhãn Nút Tiếng Việt"
        L1[Gửi Câu hỏi<br/>Submit Question]
        L2[Tải lên Tài liệu<br/>Upload Document]
        L3[Tìm kiếm Luật<br/>Search Law]
        L4[Xóa Lịch sử<br/>Clear History]
    end
```

### Form Design Patterns | Mẫu Thiết kế Form

#### Vietnamese Input Fields | Trường Input Tiếng Việt

```css
/* Vietnamese-optimized input fields */
.form-input {
    border: 2px solid #E2E8F0;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 16px;
    line-height: 1.5;
    background: white;
    transition: border-color 0.2s ease;
    min-height: 44px;
}

.form-input:focus {
    border-color: #1E40AF;
    outline: none;
    box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1);
}

/* Vietnamese text area with proper spacing */
.form-textarea {
    min-height: 120px;
    resize: vertical;
    font-family: var(--font-vietnamese);
    line-height: 1.6;
}

/* Legal document input specific styling */
.legal-input {
    font-family: var(--font-mono);
    background: #F8FAFC;
    border-left: 4px solid #F59E0B;
}
```

### Navigation Patterns | Mẫu Điều hướng

#### Vietnamese Legal Navigation | Điều hướng Pháp lý Việt Nam

```mermaid
graph TB
    subgraph "Primary Navigation | Điều hướng Chính"
        N1[Trang Chủ<br/>Home Dashboard]
        N2[Tư vấn Pháp lý<br/>Legal Consultation]
        N3[Thư viện Luật<br/>Law Library]
        N4[Tài khoản<br/>Account]
    end
    
    subgraph "Legal Categories | Danh mục Pháp lý"
        C1[Luật Dân sự<br/>Civil Law]
        C2[Luật Hình sự<br/>Criminal Law]
        C3[Luật Lao động<br/>Labor Law]
        C4[Luật Thương mại<br/>Commercial Law]
        C5[Luật Gia đình<br/>Family Law]
        C6[Luật Hành chính<br/>Administrative Law]
    end
    
    subgraph "Quick Actions | Hành động Nhanh"
        Q1[Đặt câu hỏi<br/>Ask Question]
        Q2[Tìm kiếm<br/>Search]
        Q3[Tải tài liệu<br/>Upload Document]
        Q4[Lịch sử<br/>History]
    end
```

## ♿ Accessibility Guidelines | Hướng dẫn Khả năng Tiếp cận

### WCAG 2.1 AA Compliance | Tuân thủ WCAG 2.1 AA

#### Color Contrast Requirements | Yêu cầu Tương phản Màu sắc

| Element | Contrast Ratio | Vietnamese Context |
|---------|---------------|-------------------|
| Body text | 4.5:1 minimum | Readable Vietnamese characters |
| Large text (18px+) | 3:1 minimum | Legal headers and titles |
| UI components | 3:1 minimum | Buttons and form elements |
| Focus indicators | 3:1 minimum | Keyboard navigation support |

#### Vietnamese Screen Reader Support | Hỗ trợ Đọc màn hình Tiếng Việt

```html
<!-- Proper Vietnamese language support -->
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Chatbot AI Pháp lý Việt Nam</title>
</head>

<!-- Semantic Vietnamese legal content -->
<main role="main" aria-label="Tư vấn pháp lý chính">
    <section aria-labelledby="chat-heading">
        <h1 id="chat-heading">Đặt câu hỏi pháp lý</h1>
        <div role="log" aria-live="polite" aria-label="Trả lời từ AI">
            <!-- Chat responses -->
        </div>
    </section>
</main>

<!-- Vietnamese form labels -->
<label for="legal-question">
    Nhập câu hỏi pháp lý của bạn
    <span aria-describedby="question-help">(bắt buộc)</span>
</label>
<textarea 
    id="legal-question" 
    aria-describedby="question-help"
    placeholder="Ví dụ: Tôi cần tư vấn về luật lao động..."
></textarea>
<div id="question-help" class="help-text">
    Vui lòng mô tả rõ tình huống pháp lý của bạn
</div>
```

### Keyboard Navigation | Điều hướng Bàn phím

#### Vietnamese Keyboard Shortcuts | Phím tắt Tiếng Việt

| Shortcut | Action | Vietnamese Label |
|----------|--------|------------------|
| `Ctrl + /` | Help menu | Trợ giúp |
| `Ctrl + Enter` | Submit question | Gửi câu hỏi |
| `Ctrl + D` | Toggle document panel | Bật/tắt tài liệu |
| `Ctrl + H` | View history | Xem lịch sử |
| `F1` | Accessibility help | Trợ giúp khả năng tiếp cận |

## 🎯 Design Validation Checklist | Danh sách Kiểm tra Thiết kế

### Vietnamese Legal UI Compliance | Tuân thủ UI Pháp lý Việt Nam

- [ ] **Vietnamese Text Rendering** - Proper diacritics display
- [ ] **Legal Terminology** - Accurate Vietnamese legal terms
- [ ] **Cultural Colors** - Appropriate Vietnamese color psychology
- [ ] **Formal Tone** - Professional Vietnamese communication style
- [ ] **Government Standards** - Compliance with Vietnamese UI standards
- [ ] **Accessibility** - WCAG 2.1 AA compliance for Vietnamese content
- [ ] **Performance** - Fast loading for Vietnamese users

---

*📅 Created: August 2025 | Version: 1.0 | Next: Part 2 - User Interface Layouts*

**Next Document:** [User Interface Layouts](02-user-interface-layouts.md)  
**Related:** [System Architecture](../system-architecture.md) | [User Stories](../user-stories.md)
