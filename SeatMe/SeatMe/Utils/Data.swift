//
//  Data.swift
//  SeatMe
//
//  Created by Parth Tamane on 26/10/19.
//  Copyright © 2019 Parth Tamane. All rights reserved.
//

import Foundation

func readLayout() -> RoomLayout? {
    guard let filePath = Bundle.main.path(forResource: "data", ofType: "json") else { return nil }
    let fileUrl = URL(fileURLWithPath: filePath)
    do {
        let layout = try JSONDecoder().decode(RoomLayout.self, from: Data(contentsOf: fileUrl))
        return layout
    } catch let jsonErr {
        print("Error reading the layout file.")
        print(jsonErr.localizedDescription)
    }
    return nil
}

func readLayout2() -> RoomLayout2? {
    guard let filePath = Bundle.main.path(forResource: "data_2", ofType: "json") else { return nil }
    let fileUrl = URL(fileURLWithPath: filePath)
    do {
        let layout = try JSONDecoder().decode(RoomLayout2.self, from: Data(contentsOf: fileUrl))
        return layout
    } catch let jsonErr {
        print("Error reading the layout file.")
        print(jsonErr.localizedDescription)
    }
    return nil
}

func readLayout3() -> RoomLayout3? {
    print("Called")
    guard let filePath = Bundle.main.path(forResource: "data_3", ofType: "json") else {
        print("Can't read file")
        return nil
    }
    let fileUrl = URL(fileURLWithPath: filePath)
    do {
        let layout = try JSONDecoder().decode(RoomLayout3.self, from: Data(contentsOf: fileUrl))
        return layout
    } catch let jsonErr {
        print("Error reading the layout file.")
        print(jsonErr.localizedDescription)
    }
    return nil
}
