# BOHOL 全站 WebP 图片规范与自动化处理器操作指南 (SOP)

> **核心强制标准**：
> 根据网站 SEO、GEO（生成式 AI 搜索推荐引擎优化）与 Google Core Web Vitals（页面加载速度与 LCP 性能指标）的技术要求，**网站所有图片必须严格处理为 `.webp` 格式**。
> 禁止在生产环境直接使用未经压缩优化的 `.jpg`、`.jpeg`、`.png`、`.bmp` 或 `.tiff` 格式。

---

## 一、为什么全站统一必须使用 WebP？

1. **体积缩减 70% ~ 85%**：
   在保持人眼完全不可见差异的极致画质（Quality 82）下，WebP 文件大小仅为传统 JPG/PNG 的 1/4 ~ 1/7，极大节省服务器带宽和 CDN 流量。
2. **极大提升 Google PageSpeed 与 LCP 评分**：
   Google 官方 Core Web Vitals 将 Largest Contentful Paint（最大内容渲染）作为核心排名信号。使用 WebP 能够实现毫秒级首屏加载，显著提升欧美买家浏览体验与留存率。
3. **完美兼容透明通道与无损压缩**：
   对于白底或透明底的产品扣图，WebP 原生支持 8-bit Alpha 透明通道，彻底解决传统 PNG 体积极其庞大的问题。

---

## 二、内置图片处理器工具与架构

项目在 `scripts/process_images.py` 内置了工业级图片转换处理器，具备以下核心能力：

1. **自动递归遍历**：自动扫描 `public/images/` 及其所有子目录（包括产品主图、类目图、详情图、客户评价图等）。
2. **智能色彩空间与朝向纠正**：
   - 自动读取 EXIF Orientation 并纠正旋转角度，防止手机实拍图方向倒置；
   - 智能处理 RGB、RGBA、Palette 调色板模式；
   - 剥离冗余 EXIF 元数据，保护隐私并进一步缩小体积。
3. **全站代码引用自动同步（Code Sync）**：
   - 转换完成后，处理器会自动扫描 `src/data/products/`（产品 JSON）、`src/data/journal/`（文章 Markdown）、`src/components/`、`src/pages/`、`src/layouts/` 等所有代码文件；
   - 自动将旧的 `.jpg` / `.png` 路径无缝替换为 `.webp`，无需人工逐一修改代码！
4. **安全清理源文件**：
   - 转换验证成功后自动删除无用的原始 `.jpg` / `.png` 文件，保持代码仓库纯净整洁。

---

## 三、常用命令与工作流

我们在 `package.json` 中配置了快捷脚本，团队与开发者日常可通过以下方式调用：

### 1. 一键全量转换与代码同步
当新增或替换了一批图片后，在项目根目录运行：
```bash
npm run process:images
```
*处理器将自动将所有非 WebP 图片转换为 `.webp`，自动清理原始文件，并同步更新代码中的引用。*

### 2. 实时后台监听模式（推荐在编辑/上新时开启）
如果正在密集上传图片或通过 CMS 批量拖入产品图，可启动监听模式：
```bash
npm run watch:images
```
*处理器将在后台以 2 秒为周期轮询监控 `public/images/`，一旦检测到有新的 JPG/PNG 放入，立刻秒级转为 WebP 并自动替换！*

### 3. 构建自动拦截与前置处理（Prebuild Hook）
无需担心忘记运行处理器！我们在 `package.json` 中配置了 `prebuild` 钩子：
```json
"scripts": {
  "prebuild": "python scripts/process_images.py",
  "build": "astro build"
}
```
每次执行 `npm run build` 打包发布时，系统都会**自动强制先执行图片处理器**，确保打包出来的静态站点 100% 均为 WebP 格式。

### 4. 独立审计检查命令
用于 CI/CD 检查是否存在不合规图片：
```bash
python scripts/process_images.py --check
```

---

## 四、Decap CMS 后台发布与图片上传规范

1. **管理员后台路径**：`http://localhost:4321/admin/`
2. **上传位置**：CMS 默认上传目录为 `public/images/`。
3. **日常发文建议**：
   - 若直接上传 `.webp` 图片，系统即时显示；
   - 若直接上传了 `.jpg` 或 `.png` 原图，只需触发一次 `npm run process:images`（或构建站点），系统会自动完成格式转码并保持所有文章链接有效。

---

## 五、目录规划标准

所有网站图片请分类存放于 `public/images/` 对应子目录：

| 目录路径 | 存放内容 | 建议尺寸 / 规范 |
| :--- | :--- | :--- |
| `public/images/` | 首页 Banner、工厂车间实拍、资质背书图 | 1920x1080 / 1200x800 WebP |
| `public/images/9rabbit/products/` | 产品多角度主图与白色展示底图 | 1000x1000 正方形白底 WebP |
| `public/images/9rabbit/details/` | 产品长图详情切片（S01~S08） | 800px 宽度长图 WebP |
| `public/images/9rabbit/cats/` | 行业类目导航图标与展示卡片 | 800x800 WebP |
| `public/images/reviews/` | 真实买家评价头像与使用场景反馈 | 400x400 圆形/正方形 WebP |

---
*BOHOL OEM 数字化技术中心 · 2026 年标准化执行规范*
