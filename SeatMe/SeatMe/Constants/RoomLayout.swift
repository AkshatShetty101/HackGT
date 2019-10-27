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

struct Chairs2: Decodable {
    let front: [Bool]?
    let back: [Bool]?
}

struct Table2: Decodable {
    let offset: Int
    let chairs: Chairs2
}
struct RoomLayout2: Decodable {
    let tables: [[Table2]]
    let orphans: [Bool]?
}
