# ___ Main planet updating ___ #
# organizes and coordinates calculations and variable updates

import globalFunctions as functions


def update_planets(w, h, planet_list, t_step, walls_enabled):
    default = 0
    planet_x = dict.fromkeys(planet_list, default)
    planet_y = dict.fromkeys(planet_list, default)
    collision_velocities = []

    # bounce off wall if it hits wall
    if walls_enabled:
        for planet in planet_list:
            functions.wall_collision(planet, w, h)

    current_collisions = functions.collision_detection(planet_list)  # finds collisions and returns as objects colliding

    merge_list = functions.combine_planets(current_collisions)

    if merge_list:
        for i in range(0, len(merge_list), 2):
            current_collisions.remove(merge_list[i])
            current_collisions.remove(merge_list[i + 1])
            color = [merge_list[i].R, merge_list[i].G, merge_list[i].B]
            merge_list[i + 1].merge_planet(merge_list[i].mass, merge_list[i].pos_x, merge_list[i].pos_y,
                                           color)
            planet_list.remove(merge_list[i])

    if len(current_collisions) > 1:
        # for each collision pair it finds and sets their new velocity
        for i in range(0, len(current_collisions), 2):
            # finds new velocities , puts in list
            new_velocities = functions.velocity_from_collision(current_collisions[i], current_collisions[i + 1])
            # builds list with format planet0, planet[0].vel_x and y, planet1, planet[1].vel_x and y
            collision_velocities.extend(new_velocities)

        for i in range(0, len(collision_velocities), 3):
            # finds how many collisions each object is apart of

            collision_counter = collision_velocities.count(collision_velocities[i])
            # print(i, collision_velocities[i], collision_counter)

            if collision_counter > 1:
                # finds the location of the multi collision in updateVel
                indices = [k for k, x in enumerate(collision_velocities) if x == collision_velocities[i]]
                net_object_velocity_x = 0
                net_object_velocity_y = 0
                for j in range(len(indices)):
                    # adds the velocity from each collision to get net velocity
                    net_object_velocity_x = net_object_velocity_x + collision_velocities[indices[j] + 1]
                    net_object_velocity_y = net_object_velocity_y + collision_velocities[indices[j] + 2]
                collision_velocities[i].update_velocity_x(net_object_velocity_x)
                collision_velocities[i].update_velocity_y(net_object_velocity_y)
            else:
                collision_velocities[i].update_velocity_x(collision_velocities[i + 1])
                collision_velocities[i].update_velocity_y(collision_velocities[i + 2])

    # After Collisions have been detected objects accel, vel, and position are updated accordingly
    planet_x, planet_y = functions.accel_due_to_gravity(planet_x, planet_y, planet_list)

    for i in planet_list:
        if i in current_collisions:
            i.update_accel([0, 0])
        else:
            i.update_accel([planet_x[i], planet_y[i]])

    # position update loops
    for planet in planet_list:
        if abs(planet.pos_x) > 20000:
            planet_list.remove(planet)
            continue
        elif abs(planet.pos_y) > 20000:
            planet_list.remove(planet)
            continue
        else:
            planet.update_pos(functions.position(planet, t_step))

    # velocity update loops
    for planet in planet_list:
        planet.update_vel(functions.velocity(planet, t_step))

    return merge_list
