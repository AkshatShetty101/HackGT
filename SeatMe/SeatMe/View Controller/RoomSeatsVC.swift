//
//  RoomSeatsVC.swift
//  SeatMe
//
//  Created by Parth Tamane on 26/10/19.
//  Copyright © 2019 Parth Tamane. All rights reserved.
//

import Foundation
import UIKit

class RoomSeatsVC: UIViewController {
    let ICON_WIDTH = 50
    let ICON_HEIGHT = 50
    let CHAIR_ICON_WIDTH = 30
    let CHAIR_ICON_HEIGHT = 30

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white
        view.addSubview(makeSeatsView())
        view.addSubview(makeInterestingItemsView())
    }
    
    func makeSeatsView() -> UIScrollView {
        let seatsView = UIScrollView(frame: CGRect(x: 0, y: 0, width: UIScreen.main.bounds.width, height: UIScreen.main.bounds.height/2))
        seatsView.layer.borderWidth = 1
        
        let roomLayout = readLayout()
        
        if let roomLayout = roomLayout {
            for table in roomLayout.tables {
                for chair in table.chairs {
                    var chairCoordinate = chair.coordinate
                    if chairCoordinate.x > table.coordinate.x {
                        chairCoordinate.x += ICON_WIDTH/2
                    } else {
                        chairCoordinate.x -= ICON_WIDTH/2
                    }
                    if chairCoordinate.y > table.coordinate.y {
                        chairCoordinate.y += ICON_HEIGHT/2
                    } else {
                        chairCoordinate.y -= ICON_HEIGHT/2
                    }
                    print(chairCoordinate)
                    let chairIconView = makeImageView(fileName: AssetFileNames.Chair, coordinate: chairCoordinate)
                    if chair.occupied {
                        chairIconView.image = chairIconView.image?.withRenderingMode(.alwaysTemplate)
                        chairIconView.tintColor = .red
                    }
                    seatsView.addSubview(chairIconView)
                }
                let tableIconView = makeImageView(fileName: AssetFileNames.Table, coordinate: table.coordinate)
                seatsView.addSubview(tableIconView)
            }
        }
        
        return seatsView
    }
    
    func makeInterestingItemsView() -> UIView {
        return UIView(frame: CGRect(x: 0, y: UIScreen.main.bounds.height/2, width: UIScreen.main.bounds.width, height: UIScreen.main.bounds.height/2))
    }
    
    func makeImageView(fileName: AssetFileNames, coordinate: Coordinate) -> UIImageView {
        let X_OFFSET = 100
        let Y_OFFSET = 100
        var WIDTH = ICON_WIDTH
        var HEIGHT = ICON_HEIGHT
        let icon = UIImage(named: fileName.rawValue)
        if fileName == .Chair {
            WIDTH = CHAIR_ICON_WIDTH
            HEIGHT = CHAIR_ICON_HEIGHT
        }
        let iconView = UIImageView(frame: CGRect(x: coordinate.x - WIDTH/2 + X_OFFSET, y: coordinate.y-HEIGHT/2 + Y_OFFSET, width: WIDTH, height: HEIGHT))
        iconView.image = icon
        return iconView
    }
}
