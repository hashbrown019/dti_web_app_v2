

// Function to estimate device position based on distances
function estimateDevicePosition(distances) {
	if (distances.length < 3) {
		throw new Error('At least three distances are required for trilateration.');
	}

	// Trilateration
	const position = trilaterate(distances);

	return position;
}

// Function to perform trilateration
function trilaterate(distances) {
	const n = distances.length;

	// Initialize variables for trilateration calculations
	let sumWeights = 0;
	let weightedX = 0;
	let weightedY = 0;

	// Iterate through pairs of distances
	for (let i = 0; i < n - 1; i++) {
		for (let j = i + 1; j < n; j++) {
			const d1 = distances[i];
			const d2 = distances[j];

			const weight = 1 / d1; // Use distance as weight

			// Calculate intersection point weights
			sumWeights += weight;
			weightedX += weight * ((d1 * d1 - d2 * d2) + (d1 * d1)) / (2 * d1);
			weightedY += weight * Math.sqrt(d1 * d1 - weightedX * weightedX);
		}
	}

	// Calculate the weighted average of intersection points
	const intersectionX = weightedX / sumWeights;
	const intersectionY = weightedY / sumWeights;

	return { x: intersectionX, y: intersectionY };
}

// Estimate the device position

function get_item_coordinates(distances){

	const estimatedPosition = estimateDevicePosition(distances);

	// Output estimated device position

	// Output coordinates of beacons relative to the device
	const beaconCoordinates = distances.map((distance, index) => {
		return {
			x: estimatedPosition.x + distance,
			y: estimatedPosition.y
		};
	});

	return {
		"device" : estimatedPosition,
		"beacons" : beaconCoordinates,
	}
}


// Example data (simulated distances)
// const distances_ = [5, 7, 8]; // Replace with your actual distances
// var res = get_item_coordinates(distances_)
// console.log(res)