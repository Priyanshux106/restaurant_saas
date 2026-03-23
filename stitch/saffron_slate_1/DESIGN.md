# Design System Specification: The Culinary Editorial

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"The Sensory Editorial."** 

This system moves away from the clinical, "app-like" structures of standard food delivery platforms and instead adopts the sophisticated layout of a high-end gastronomic journal. We treat food as art and whitespace as a canvas. To achieve this, we break the traditional grid through **intentional asymmetry**: overlapping high-quality photography with oversized typography, and using tonal layering rather than structural lines. The goal is an experience that feels curated, warm, and expensive.

## 2. Colors
Our palette is rooted in the heat and earthiness of spices, balanced by a clean, breathable foundation.

*   **Primary (#b7102a) & Secondary (#8e4e14):** These represent the "Spice" in the brand. Use the Primary for high-action CTAs and the Secondary for subtle brand accents or earthy backgrounds.
*   **The "No-Line" Rule:** To maintain an editorial feel, **1px solid borders are strictly prohibited for sectioning.** All visual boundaries must be created through background color shifts. For example, a menu section using `surface_container_low` (#f5f3f3) should sit directly against a `surface` (#fbf9f9) background.
*   **Surface Hierarchy & Nesting:** Depth is achieved by "stacking" surface tiers.
    *   **Level 0 (Base):** `surface` (#fbf9f9)
    *   **Level 1 (Sections):** `surface_container_low` (#f5f3f3)
    *   **Level 2 (Interactive Cards):** `surface_container_lowest` (#ffffff)
*   **The "Glass & Gradient" Rule:** Use `surface_tint` at 10-15% opacity with a `backdrop-blur` for floating navigation bars. For primary hero sections, apply a subtle linear gradient from `primary` (#b7102a) to `primary_container` (#db313f) to add depth and movement to the "heat" of the brand.

## 3. Typography
The typography system relies on the tension between a premium serif and a functional sans-serif.

*   **The Voice (Playfair Display/Noto Serif):** Used for `display` and `headline` scales. This is our "Chef’s Signature." It should feel bold and authoritative. Use `display-lg` (3.5rem) for hero titles, often overlapping image edges to create an editorial "magazine" feel.
*   **The Clarity (Inter):** Used for `title`, `body`, and `label` scales. This is our "Service Staff"—unobtrusive, highly legible, and helpful. 
*   **Hierarchy Note:** Always prioritize generous leading (line-height) in body text to ensure the "generous whitespace" requested by the brand is felt even within the copy.

## 4. Elevation & Depth
In this design system, depth is a result of light and layering, not artificial containers.

*   **The Layering Principle:** Avoid the "floating box" look. Instead, achieve elevation by placing a `surface_container_lowest` (#ffffff) element on a `surface_container` (#efeded) background. This creates a soft, natural lift.
*   **Ambient Shadows:** When a physical lift is required (e.g., a floating cart or a modal), use a shadow tinted with `on_surface` (#1b1c1c). 
    *   **Specs:** Blur: 24px-40px, Opacity: 4%-6%, Y-Offset: 8px. It should look like a soft glow of shadow, not a hard edge.
*   **The "Ghost Border" Fallback:** If a border is required for accessibility (e.g., input fields), use the `outline_variant` (#e4bebc) at 20% opacity. Never use 100% opaque borders.
*   **Asymmetric Overlaps:** To break the template look, place images such that they bleed off the edge of the container or overlap a typography block by `spacing-8` (2.75rem).

## 5. Components

### Buttons
*   **Primary:** Background `primary` (#b7102a) with `on_primary` (#ffffff) text. Use `rounded-md` (0.375rem).
*   **Secondary:** Background `secondary_container` (#ffab69) with `on_secondary_container` (#783d01).
*   **Interaction:** On hover, shift the background color one step in the tier (e.g., Primary to `primary_container`).

### Cards & Menu Items
*   **Rule:** No dividers. Use `spacing-10` (3.5rem) of vertical whitespace to separate items.
*   **Styling:** Use `surface_container_low` (#f5f3f3) as the base. Images should have a `rounded-lg` (0.5rem) corner to feel soft yet modern.

### Input Fields
*   **Styling:** Use a `surface_container_highest` (#e4e2e2) background with no border.
*   **Focus State:** A 2px bottom-border using `primary` (#b7102a). Avoid surrounding the entire box on focus.

### Chips (Dietary Tags)
*   **Styling:** Use `tertiary_container` (#008379) for "Vegan" or "Healthy" tags to provide a cool contrast to the warm reds. Use `rounded-full` (9999px) and `label-md` typography.

### Floating Action (Booking/Cart)
*   **Glassmorphism:** Use a semi-transparent `surface_bright` (#fbf9f9) with a 12px backdrop-blur and a "Ghost Border" at 10% opacity.

## 6. Do's and Don'ts

### Do:
*   **Do** use asymmetrical layouts where text and high-quality photography overlap.
*   **Do** use the full range of the spacing scale—specifically `spacing-16` (5.5rem) and `spacing-20` (7rem)—to create "breathing room" between major sections.
*   **Do** use `primary_fixed_dim` for subtle background accents behind food photography to make the reds "pop."

### Don't:
*   **Don't** use lines or dividers to separate content. Use whitespace and tonal shifts.
*   **Don't** use pure black for text. Always use `on_surface` (#1b1c1c) to maintain a premium, softened look.
*   **Don't** use "Standard" shadows. If an element doesn't feel like it's lifting naturally through color, reconsider its placement.
*   **Don't** crowd the photography. If an image is present, let it occupy at least 40% of the viewport width.