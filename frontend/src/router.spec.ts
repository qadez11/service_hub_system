import { describe, expect, it } from "vitest"

import { router } from "./router"

describe("frontend routes", () => {
	it("resolves the existing fallback route", () => {
		const resolved = router.resolve("/missing-route")

		expect(resolved.matched).toHaveLength(1)
		expect(resolved.matched[0]?.path).toBe("/:path(.*)*")
	})
})
