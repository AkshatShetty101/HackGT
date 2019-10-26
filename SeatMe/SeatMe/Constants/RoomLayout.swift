//
//  RoomLayout.swift
//  SeatMe
//
//  Created by Parth Tamane on 26/10/19.
//  Copyright © 2019 Parth Tamane. All rights reserved.
//

import Foundation


struct Coordinate: Decodable {
    var x: Int
    var y: Int
}

struct Chair: Decodable {
    let coordinate: Coordinate
    let occupied: Bool
}

struct Table: Decodable {
    let coordinate: Coordinate
    let chairs: [Chair]
}

struct RoomLayout: Decodable {
    let tables: [Table]
}