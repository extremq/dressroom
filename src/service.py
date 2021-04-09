from pyservice import Service

from drawer import get_pose, get_fur, get_costume, get_section_name


service = Service("dressroom")
SVG_DEF = '<svg xmlns="http://www.w3.org/2000/svg" \
				height="80px" width="60px">'


@service.on_request("fur")
async def draw_fur(request):
	fur = get_fur(request.fur)
	if fur is None:
		await request.reject(
			"NotFound",
			"Fur {} not found.".format(request.fur)
		)
		return

	pose = get_pose("statique")
	await request.send("".join([
		SVG_DEF,
		fur.asset,
		fur.generate_color(request.color),
		fur.pose_asset,
		pose.generate(None),
		"</svg>"
	]))


@service.on_request("costume")
async def draw_costume(request):
	costume = get_costume(request.section, request.costume)
	if costume is None:
		await request.reject(
			"NotFound",
			"Costume {} not found in section {}."
			.format(request.costume, request.section)
		)
		return

	await request.send("".join([
		SVG_DEF,
		costume.asset,
		*costume.generate_color(request.colors),
		costume.render,
		"</svg>"
	]))


@service.on_request("mouse")
async def draw_mouse(request):
	fur = get_fur(request.fur)
	if fur is None:
		await request.reject(
			"NotFound",
			"Fur {} not found.".format(request.fur)
		)
		return

	costumes = []
	for section, (costume_id, colors) in enumerate(request.costumes):
		if costume_id == 0:
			continue

		section_name = get_section_name(section)
		costume = get_costume(section_name, costume_id)
		if costume is None:
			await request.reject(
				"NotFound",
				"Costume {} not found in section {}."
				.format(costume_id, section_name)
			)
			return

		costumes.append((costume, colors))

	pose = get_pose("statique")

	await request.send("".join([
		SVG_DEF,

		fur.asset,
		fur.generate_color(request.fur_color),

		"".join(
			costume.asset
			for costume, _ in costumes
		),
		"".join(
			"".join(costume.generate_color(colors))
			for costume, colors in costumes
		),

		fur.pose_asset,
		pose.generate(costumes),

		"</svg>"
	]))


if __name__ == "__main__":
	service.run()
