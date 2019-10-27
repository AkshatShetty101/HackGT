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
    let CHAIR_ICON_WIDTH = 20
    let CHAIR_ICON_HEIGHT = 20
    let TABLE_ICON_WIDTH = 50
    let TABLE_ICON_HEIGHT = 50
    let GUTTER_HEIGHT = 10
    var roomDetailsTableView: UITableView?
    let roomCellID = "RoomListCell"
    var layout: RoomLayout2? = nil
    var seatsView: UIScrollView?
    var timer = Timer()
    var maxX: CGFloat = 0
    var maxY: CGFloat = 0
    
    let roomFacilities = ["Printer", "Fire Exit", "Projector"]
    let roomFacilitiesIcon:[UIImage?] = [UIImage(named: "printer"), UIImage(named: "fire-exit"), UIImage(named: "projector")]
    
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white
        view.addSubview(makeLayoutHeaderView())
        seatsView = UIScrollView(frame: CGRect(x: 10, y: 50, width: UIScreen.main.bounds.width - 10, height: UIScreen.main.bounds.height/2))
        view.addSubview(seatsView!)
        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true, block: { (timer) in
            self.makeSeatsView()
        })
//        makeSeatsView()
        
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
    
    func makeSeatsView() {
        seatsView!.subviews.forEach({ $0.removeFromSuperview() }) // this gets things done

        let _ = fetchLayout { (layout) in
            print(layout)
            var rowNumber = 0
            var maxRowLength = 0
            var offset = 0
            for row in (layout.tables) {
                let sortedRow = row.sorted(by: {$0.offset < $1.offset})
                if sortedRow.count > 0 {
                    offset = sortedRow[0].offset
                }
                maxRowLength = sortedRow.count > maxRowLength ? sortedRow.count : maxRowLength
//                print(row)
                for table in sortedRow {
//                    print(table)
                    self.makeImageView2(rowNumber: rowNumber, offset: table.offset < offset ? offset : table.offset, chairs: table.chairs) { (imageViews) in
                        
                        for imageView in imageViews {
                            DispatchQueue.main.async {
                                self.seatsView?.addSubview(imageView)
                            }
                        }
                    }
                    
                    offset += 1
                }
                rowNumber += 1
            }
           
            DispatchQueue.main.async {
                let size = CGSize(width:2*maxRowLength*self.TABLE_ICON_WIDTH, height: rowNumber*(self.TABLE_ICON_HEIGHT + 2*self.CHAIR_ICON_HEIGHT)+self.CHAIR_ICON_HEIGHT+self.GUTTER_HEIGHT)
                print(2*maxRowLength*self.TABLE_ICON_WIDTH)
                self.seatsView?.contentSize = CGSize(width: 2*offset*self.TABLE_ICON_WIDTH, height: rowNumber*(self.TABLE_ICON_HEIGHT + 2*self.CHAIR_ICON_HEIGHT)+self.CHAIR_ICON_HEIGHT+self.GUTTER_HEIGHT)
                self.seatsView?.layer.borderWidth = 1
                self.maxX = size.width
                self.maxY = size.height
                if let orphans = layout.orphans {
                    self.addOrphans(orphans: orphans)
                }
            }
        }
    }
    
    func readFromCoordinatedLayout(seatsView: UIScrollView) {
     let roomLayout = readLayout()
            var maxX = 0
            var maxY = 0
            
            if let roomLayout = roomLayout {
                for table in roomLayout.tables {
                    for chair in table.chairs {
                        let chairCoordinate = chair.coordinate
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
    
    func makeImageView2(rowNumber: Int, offset: Int, chairs: Chairs2, completion: @escaping ([UIImageView]) -> () ) -> [UIImageView] {
        print(chairs)
        
        var imageViews: [UIImageView] = []
        let tableIcon = UIImage(named: AssetFileNames.Table.rawValue)
        DispatchQueue.main.async {
            let tableIconView = UIImageView(frame: CGRect(x: offset*2*self.TABLE_ICON_WIDTH + self.GUTTER_HEIGHT, y: rowNumber*(self.TABLE_ICON_HEIGHT+2*self.CHAIR_ICON_HEIGHT)+self.CHAIR_ICON_HEIGHT, width: 2*self.TABLE_ICON_WIDTH - self.GUTTER_HEIGHT, height: self.TABLE_ICON_HEIGHT))
            NSLayoutConstraint.activate([
                tableIconView.widthAnchor.constraint(equalToConstant: CGFloat(self.TABLE_ICON_WIDTH*2)),
                tableIconView.heightAnchor.constraint(equalToConstant: CGFloat(self.TABLE_ICON_HEIGHT))
            ])
            tableIconView.image = tableIcon
            imageViews.append(tableIconView)
            
            
            var yOffset = rowNumber*(self.TABLE_ICON_HEIGHT+2*self.CHAIR_ICON_HEIGHT)-self.GUTTER_HEIGHT
              
              var colCount = 0
              if let frontChairs = chairs.front {
                  for chair in frontChairs {
                      if colCount == 2 {
                          break;
                      }
                   
                      let chairIcon = UIImage(named: AssetFileNames.Chair.rawValue)
                      let chairIconView = UIImageView(frame: CGRect(x: offset*100+20*(colCount+1)+10*colCount, y: yOffset, width: self.CHAIR_ICON_WIDTH, height: self.CHAIR_ICON_HEIGHT))
                      chairIconView.image = chairIcon
                      chairIconView.image = chairIconView.image?.withRenderingMode(.alwaysTemplate)
                      chairIconView.tintColor = !chair ? confirmGreen : disabledRed
                      imageViews.append(chairIconView)
                      
                      colCount += 1
                  }
              }
              
            yOffset = (rowNumber+1)*(self.TABLE_ICON_HEIGHT+self.CHAIR_ICON_HEIGHT) + rowNumber*self.CHAIR_ICON_HEIGHT - self.GUTTER_HEIGHT
              
              colCount = 0
              if let backChairs = chairs.back {
                  for chair in backChairs {
                     if colCount == 2 {
                         break;
                     }

                     let chairIcon = UIImage(named: AssetFileNames.Chair.rawValue)
                    let chairIconView = UIImageView(frame: CGRect(x: offset*100+20*(colCount+1)+10*colCount, y: yOffset, width: self.CHAIR_ICON_WIDTH, height: self.CHAIR_ICON_HEIGHT))
                     chairIconView.image = chairIcon
                     chairIconView.image = chairIconView.image?.withRenderingMode(.alwaysTemplate)
                     chairIconView.tintColor = !chair ? confirmGreen : disabledRed
                     imageViews.append(chairIconView)
                         
                     colCount += 1

                 }
              }
            
            completion(imageViews)
        }
        return imageViews
    }
    
    func addOrphans(orphans:[Bool]) {
        var x: CGFloat = 0
        var y: CGFloat = self.maxY
        for orphan in orphans {
            if x > maxX {
                x = 0
                y += CGFloat(self.CHAIR_ICON_HEIGHT)
            }
            
            DispatchQueue.main.async {
                let chairIcon = UIImage(named: AssetFileNames.Chair.rawValue)
                let chairIconView = UIImageView(frame: CGRect(x: x, y: y, width: CGFloat(self.CHAIR_ICON_WIDTH), height: CGFloat(self.CHAIR_ICON_HEIGHT)))
                chairIconView.image = chairIcon
                chairIconView.image = chairIconView.image?.withRenderingMode(.alwaysTemplate)
                chairIconView.tintColor = !orphan ? confirmGreen : disabledRed
                self.seatsView?.addSubview(chairIconView)
                x += CGFloat(self.CHAIR_ICON_WIDTH + self.GUTTER_HEIGHT)
            }
            
            maxY = y
       
        }
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
    
    func fetchLayout(completion: @escaping (RoomLayout2) -> ()) {
        let url = URL(string: "http://127.0.0.1:5000/layout?id=1")!

        let task = URLSession.shared.dataTask(with: url) {(data, response, error) in
            guard let data = data else { return }
            do {
                let data = try JSONDecoder().decode(RoomLayout2.self, from: data)
                completion(data)
               } catch let jsonErr {
                   print("Error reading the data file.")
                   print(jsonErr.localizedDescription)
               }
        }

        task.resume()
    }
}
