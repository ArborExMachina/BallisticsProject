
SELECT y.bc, y.muzzle_velocity, y.zero, y.range, y.elevation
FROM Dump y
JOIN (
	SELECT bc, muzzle_velocity, zero, MAX(elevation) as max_el 
	FROM Dump 
	WHERE elevation <= 1.5 
	GROUP BY bc, muzzle_velocity
) x ON x.bc = y.bc AND x.muzzle_velocity = y.muzzle_velocity
WHERE y.elevation = max_el
GROUP BY y.bc, y.muzzle_velocity, y.zero
ORDER BY y.bc, y.muzzle_velocity, range DESC
