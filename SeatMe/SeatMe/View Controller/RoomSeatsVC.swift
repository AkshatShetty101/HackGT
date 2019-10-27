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
    let CHAIR_ICON_WIDTH = 30
    let CHAIR_ICON_HEIGHT = 30
    let TABLE_ICON_WIDTH = 50
    let TABLE_ICON_HEIGHT = 50
    let GUTTER_HEIGHT = 10
    var roomDetailsTableView: UITableView?
    let roomCellID = "RoomListCell"

    let roomFacilities = ["Printer", "Fire Exit", "Projector"]
    let roomFacilitiesIcon:[UIImage?] = [UIImage(named: "printer"), UIImage(named: "fire-exit"), UIImage(named: "projector")]
    
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white
        view.addSubview(makeLayoutHeaderView())
        view.addSubview(makeSeatsView())
        view.addSubview(makeFacilitiesHeaderView())
        view.addSubview(makeTableView())
    }
    
    func makeLayoutHeaderView() -> UIView {
        let title = UILabel(frame: CGRect(x: 0, y: 0, width: UIScreen.main.bounds.width, height: 50))
        title.text = "Room Layout"
        title.font = UIFont(name: "HelveticaNeue-Bold", size: 18)
        title.textAlignment = .center
        title.textColor = darkGrey
        return title
    }
    
    func makeFacilitiesHeaderView() -> UIView {
        let title = UILabel(frame: CGRect(x: 0, y: UIScreen.main.bounds.height/2 + 50, width: UIScreen.main.bounds.width, height: 50))
        title.text = "Facilities"
        title.font = UIFont(name: "HelveticaNeue-Bold", size: 18)
        title.textAlignment = .center
        title.textColor = darkGrey
        return title
    }
    
    func makeSeatsView() -> UIScrollView {
        let seatsView = UIScrollView(frame: CGRect(x: 0, y: 50, width: UIScreen.main.bounds.width, height: UIScreen.main.bounds.height/2))
        let layout = readLayout2()
        var rowNumber = 0
        var maxRowLength = 0
        for row in (layout?.tables)! {
            var offset = 0
            maxRowLength = row.count > maxRowLength ? row.count : maxRowLength

            for table in row {
                
                for imageView in makeImageView2(rowNumber: rowNumber, offset: table.offset , chairs: table.chairs) {
                    seatsView.addSubview(imageView)
                }
                offset += 1
            }
            rowNumber += 1
        }
        let size = CGSize(width:2*maxRowLength*TABLE_ICON_WIDTH, height: rowNumber*(TABLE_ICON_HEIGHT + 2*CHAIR_ICON_HEIGHT)+CHAIR_ICON_HEIGHT+GUTTER_HEIGHT)
        print(size)
        seatsView.contentSize = size
        return seatsView
    }
    
    func readFromCoordinatedLayout(seatsView: UIScrollView) {
     let roomLayout = readLayout()
            var maxX = 0
            var maxY = 0
            
            if let roomLayout = roomLayout {
                for table in roomLayout.tables {
                    for chair in table.chairs {
                        var chairCoordinate = chair.coordinate
                        if chairCoordinate.x > maxX {
                            maxX = chairCoordinate.x
                        }
                        if chairCoordinate.y > maxY {
                            maxY = chairCoordinate.y
                        }
                        
    //                    if chairCoordinate.x > table.coordinate.x {
    //                        chairCoordinate.x += ICON_WIDTH/2
    //                    } else {
    //                        chairCoordinate.x -= ICON_WIDTH/2
    //                    }
    //                    if chairCoordinate.y > table.coordinate.y {
    //                        chairCoordinate.y += ICON_HEIGHT/2
    //                    } else {
    //                        chairCoordinate.y -= ICON_HEIGHT/2
    //                    }
                        print(chairCoordinate)
                        let chairIconView = makeImageView(fileName: AssetFileNames.Chair, coordinate: chairCoordinate)
                        if chair.occupied {
                            chairIconView.tintColor = disabledRed
                        } else {
                            chairIconView.tintColor = confirmGreen
                        }
                        seatsView.addSubview(chairIconView)
                    }
                    if table.coordinate.x > maxX {
                        maxX = table.coordinate.x
                    }
                    if table.coordinate.y > maxY {
                        maxY = table.coordinate.y
                    }
                    
                    let tableIconView = makeImageView(fileName: AssetFileNames.Table, coordinate: table.coordinate)
                    tableIconView.tintColor = darkGrey
                    seatsView.addSubview(tableIconView)
                }
            }
            print(maxX," ",maxY)
    }
    
    func makeTableView() -> UITableView {
        roomDetailsTableView = UITableView(frame: CGRect(x: 0, y: UIScreen.main.bounds.height/2 + 100, width: UIScreen.main.bounds.width, height: UIScreen.main.bounds.height/2))
        guard let roomDetailsTableView = roomDetailsTableView else { return UITableView(frame: CGRect(x: 0, y: UIScreen.main.bounds.height/2, width: UIScreen.main.bounds.width, height: UIScreen.main.bounds.height/2))}
        roomDetailsTableView.register(UITableViewCell.self, forCellReuseIdentifier: roomCellID)
        roomDetailsTableView.dataSource = self
        roomDetailsTableView.delegate = self
        return roomDetailsTableView
    }
    
    func makeImageView(fileName: AssetFileNames, coordinate: Coordinate) -> UIImageView {
        let X_OFFSET = 0
        let Y_OFFSET = 0
        var WIDTH = TABLE_ICON_WIDTH
        var HEIGHT = TABLE_ICON_HEIGHT
        let icon = UIImage(named: fileName.rawValue)
        if fileName == .Chair {
            WIDTH = CHAIR_ICON_WIDTH
            HEIGHT = CHAIR_ICON_HEIGHT
        }
        let iconView = UIImageView(frame: CGRect(x: coordinate.x - WIDTH/2 + X_OFFSET, y: coordinate.y-HEIGHT/2 + Y_OFFSET, width: WIDTH, height: HEIGHT))
        iconView.image = icon
        iconView.image = iconView.image?.withRenderingMode(.alwaysTemplate)
        
        return iconView
    }
    
    func makeImageView2(rowNumber: Int, offset: Int, chairs: Chairs2 ) -> [UIImageView] {
      
        
        var imageViews: [UIImageView] = []
        let tableIcon = UIImage(named: AssetFileNames.Table.rawValue)
        let tableIconView = UIImageView(frame: CGRect(x: offset*2*TABLE_ICON_WIDTH, y: rowNumber*(TABLE_ICON_HEIGHT+2*CHAIR_ICON_HEIGHT)+CHAIR_ICON_HEIGHT, width: 2*TABLE_ICON_WIDTH, height: TABLE_ICON_HEIGHT))
        tableIconView.image = tableIcon
        imageViews.append(tableIconView)
        
        var yOffset = rowNumber*(TABLE_ICON_HEIGHT+2*CHAIR_ICON_HEIGHT)+GUTTER_HEIGHT
        
        var colCount = 0
        for chair in chairs.front {
            if colCount == 2 {
                break;
            }
            let chairIcon = UIImage(named: AssetFileNames.Chair.rawValue)
            let chairIconView = UIImageView(frame: CGRect(x: offset*100+20*(colCount+1)+10*colCount, y: yOffset, width: CHAIR_ICON_WIDTH, height: CHAIR_ICON_HEIGHT))
            chairIconView.image = chairIcon
            chairIconView.image = chairIconView.image?.withRenderingMode(.alwaysTemplate)
            chairIconView.tintColor = !chair ? confirmGreen : disabledRed
            imageViews.append(chairIconView)
            
            colCount += 1
//            if chairs[1] != -1 {
//                let chairIcon = UIImage(named: AssetFileNames.Chair.rawValue)
//                let chairIconView = UIImageView(frame: CGRect(x: offset*100+50, y: yOffset, width: CHAIR_ICON_WIDTH, height: CHAIR_ICON_HEIGHT))
//                chairIconView.image = chairIcon
//                chairIconView.image = chairIconView.image?.withRenderingMode(.alwaysTemplate)
//                chairIconView.tintColor = chairs[0] == 0 ? confirmGreen : disabledRed
//                imageViews.append(chairIconView)
//            }
        }
        

        yOffset = (rowNumber+1)*(TABLE_ICON_HEIGHT+CHAIR_ICON_HEIGHT) + rowNumber*CHAIR_ICON_HEIGHT - GUTTER_HEIGHT
        
        colCount = 0
        for chair in chairs.back {
            if colCount == 2 {
                break;
            }

            let chairIcon = UIImage(named: AssetFileNames.Chair.rawValue)
            let chairIconView = UIImageView(frame: CGRect(x: offset*100+20*(colCount+1)+10*colCount, y: yOffset, width: CHAIR_ICON_WIDTH, height: CHAIR_ICON_HEIGHT))
            chairIconView.image = chairIcon
            chairIconView.image = chairIconView.image?.withRenderingMode(.alwaysTemplate)
            chairIconView.tintColor = !chair ? confirmGreen : disabledRed
            imageViews.append(chairIconView)
                
            colCount += 1
//            if chairs[1] != -1 {
//                let chairIcon = UIImage(named: AssetFileNames.Chair.rawValue)
//                let chairIconView = UIImageView(frame: CGRect(x: offset*100+50, y: yOffset, width: CHAIR_ICON_WIDTH, height: CHAIR_ICON_HEIGHT))
//                chairIconView.image = chairIcon
//                chairIconView.image = chairIconView.image?.withRenderingMode(.alwaysTemplate)
//                chairIconView.tintColor = chairs[0] == 0 ? confirmGreen : disabledRed
//                imageViews.append(chairIconView)
//            }
        }
        
//        if chairs[2] != -1 {
//            let chairIcon = UIImage(named: AssetFileNames.Chair.rawValue)
//            let chairIconView = UIImageView(frame: CGRect(x: offset*100+20, y: yOffset, width: CHAIR_ICON_WIDTH, height: CHAIR_ICON_HEIGHT))
//            chairIconView.image = chairIcon
//            chairIconView.image = chairIconView.image?.withRenderingMode(.alwaysTemplate)
//            chairIconView.tintColor = chairs[0] == 0 ? confirmGreen : disabledRed
//            imageViews.append(chairIconView)
//        }
//
//        if chairs[3] != -1 {
//            let chairIcon = UIImage(named: AssetFileNames.Chair.rawValue)
//            let chairIconView = UIImageView(frame: CGRect(x: offset*100+50, y: yOffset, width: CHAIR_ICON_WIDTH, height: CHAIR_ICON_HEIGHT))
//            chairIconView.image = chairIcon
//            chairIconView.image = chairIconView.image?.withRenderingMode(.alwaysTemplate)
//            chairIconView.tintColor = chairs[0] == 0 ? confirmGreen : disabledRed
//            imageViews.append(chairIconView)
//        }
               
        return imageViews
    }
}

extension RoomSeatsVC: UITableViewDelegate {
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 80
    }
}

extension RoomSeatsVC: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return roomFacilitiesIcon.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: roomCellID, for: indexPath)
        let facilityImageView = UIImageView(frame: CGRect(x: 0, y: 0, width: 40, height: 40))
        facilityImageView.clipsToBounds = true
        facilityImageView.contentMode = .scaleAspectFit
        facilityImageView.image = roomFacilitiesIcon[indexPath.row]
        NSLayoutConstraint.activate([facilityImageView.widthAnchor.constraint(equalToConstant: 40)])
        let facilityNameLbl = UILabel()
        facilityNameLbl.text = roomFacilities[indexPath.row]
        facilityNameLbl.font = UIFont(name: "HelveticaNeue-Light", size: 16)
        
        let contentStackView = UIStackView(arrangedSubviews: [facilityImageView, facilityNameLbl])
        contentStackView.distribution = .fillProportionally
        cell.addSubview(contentStackView)
        contentStackView.translatesAutoresizingMaskIntoConstraints = false
        
        NSLayoutConstraint.activate([
            contentStackView.leadingAnchor.constraint(equalTo: cell.leadingAnchor, constant: 10),
            contentStackView.trailingAnchor.constraint(equalTo: cell.trailingAnchor, constant: -10),
            contentStackView.topAnchor.constraint(equalTo: cell.topAnchor, constant: 10),
            contentStackView.bottomAnchor.constraint(equalTo: cell.bottomAnchor, constant: 10)
        ])
        return cell
    }
}
