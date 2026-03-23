# Design System Document: The Culinary Editorial

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"The Sensory Atelier."** 

Moving away from the cluttered, "fast-food" grid layouts common in the industry, this system treats digital real estate like a high-end food journal or a curated gallery space. We balance the heat of the "Spice House" brand with the cooling precision of a minimalist editorial. The experience is defined by **intentional asymmetry**, where large-scale serif typography breaks the container, and high-contrast tonal shifts replace traditional borders. We are not just building a menu; we are building an appetite.

---

## 2. Colors: Tonal Heat & Culinary Depth
Our palette is a study in "Warmth on White." We use the heat of reds and oranges to draw the eye to action, while the "Mint-White" (`#f3fcf0`) background provides a palate cleanser.

### The "No-Line" Rule
**Explicit Instruction:** Designers are prohibited from using 1px solid borders to section content. Boundaries must be defined solely through:
1.  **Background Shifts:** Placing a `surface_container_low` (`#edf6ea`) section against a `surface` (`#f3fcf0`) background.
2.  **Generous Negative Space:** Using the `12` (4rem) or `16` (5.5rem) spacing tokens to create mental "rooms" for content.

### Surface Hierarchy & Nesting
Treat the UI as a series of fine paper layers. 
*   **The Base:** `surface` (`#f3fcf0`) is the canvas.
*   **The Plating:** `surface_container_low` (`#edf6ea`) is for secondary content areas.
*   **The Feature:** `surface_container_lowest` (`#ffffff`) is reserved for high-priority cards or modals to create a "brilliant white" lift.

### The "Glass & Gradient" Rule
To avoid a flat, "out-of-the-box" look, use **Glassmorphism** for floating navigation bars or filter overlays. Use `surface` at 80% opacity with a `backdrop-blur` of 20px. 
*   **Signature Texture:** Main CTAs should utilize a subtle linear gradient from `primary` (`#b7102a`) to `primary_container` (`#db313f`) at a 135-degree angle to mimic the natural sheen of glazed spices.

---

### 3. Typography: The Editorial Voice
We utilize a high-contrast pairing to evoke the feeling of a premium printed menu.

*   **Display & Headlines (Noto Serif / Playfair Equivalent):**
    *   `display-lg` (3.5rem): Used for hero titles and "Spice House" branding moments. Always set with a tight letter-spacing (-0.02em).
    *   `headline-md` (1.75rem): Used for dish names. It communicates authority and tradition.
*   **Body & Labels (Manrope / Montserrat Equivalent):**
    *   `body-lg` (1rem): Used for dish descriptions. Ensure a line-height of 1.6 to maintain "breathing room."
    *   `label-md` (0.75rem): All-caps with 0.05em tracking for "Price" or "Category" tags to provide a functional, modern contrast to the serif headings.

---

## 4. Elevation & Depth: Tonal Layering
Traditional shadows are often too "digital." We use **Ambient Heat** to define depth.

*   **The Layering Principle:** Instead of a shadow, place a `surface_container_highest` (`#dce5d9`) element behind a `surface_container_lowest` (`#ffffff`) card. This creates a soft, natural lift reminiscent of architectural lighting.
*   **Ambient Shadows:** For floating action buttons or elevated modals, use a shadow with a 40px blur and 6% opacity. The shadow color must be a tint of `secondary` (`#7d562d`) rather than pure black, ensuring the shadow feels like a "warm glow" on the table.
*   **The "Ghost Border" Fallback:** If a divider is essential for accessibility, use the `outline_variant` (`#e4bebc`) at 15% opacity. It should be felt, not seen.

---

## 5. Components: Crafted Primitives

### Buttons (The "Glaze" Style)
*   **Primary:** Gradient fill (`primary` to `primary_container`), `rounded-md` (0.375rem). No border. Label in `on_primary` (`#ffffff`).
*   **Secondary:** Ghost style. No fill, `outline` token at 20% opacity. Label in `primary`.
*   **Tertiary:** Text-only, `label-md` style, with a 2px underline in `secondary_fixed` (`#ffdcbd`).

### Cards & Lists (The "Plated" Approach)
*   **Dish Cards:** Forbid the use of divider lines. Use `surface_container_low` cards on a `surface` background. The image should be slightly offset or "bleed" over the edge of the card to break the rigid box.
*   **Navigation:** Use `surface_bright` with a backdrop blur for the top nav.

### Specialized Component: The "Spice Meter"
*   A custom horizontal slider using `primary` for high-heat dishes and `secondary_container` for mild dishes. The "thumb" should be a `surface_container_lowest` circle with a `primary` glow shadow.

---

## 6. Do's and Don'ts

### Do:
*   **Do** allow typography to overlap image containers slightly (using negative margins) to create a high-end magazine feel.
*   **Do** use `primary_fixed` (`#ffdad8`) as a soft background for "Chef's Specials" or "Limited Time" callouts.
*   **Do** ensure all food photography is high-key and uses the `surface` color in its styling.

### Don't:
*   **Don't** use 100% black text. Always use `on_surface` (`#161d16`) for a softer, premium charcoal feel.
*   **Don't** use the `DEFAULT` roundedness (0.25rem) for everything. Use `none` for hero images and `xl` (0.75rem) for interactive chips to create a sophisticated "mixed geometry."
*   **Don't** use standard "Success" greens. If a dish is available, use subtle typography; if it's "Spicy," use the `primary` red.

---

**Director’s Final Note:** This design system succeeds when the user feels they are being served, not just navigating a site. Keep the spacing aggressive and the colors appetizing. If it feels too "boxy," add more white space. If it feels too "cold," increase the use of the `primary_container` accents.