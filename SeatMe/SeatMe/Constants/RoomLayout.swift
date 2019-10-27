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


struct Centroid: Decodable {
    let x: Int
    let y: Int
}

struct Chair3: Decodable {
    let cid: String
    let centroid: Centroid
    let occupied: Bool
}

struct Size: Decodable {
    let w: Int
    let h: Int
}

struct Table3: Decodable {
    let tid: Int
    let centroid: Centroid
    let chairs: [Chair3]
}

struct RoomLayout3: Decodable {
    let size: Size
    let tables: [Table3]
}
