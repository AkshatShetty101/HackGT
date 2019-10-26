//
//  ViewController.swift
//  SeatMe
//
//  Created by Parth Tamane on 26/10/19.
//  Copyright © 2019 Parth Tamane. All rights reserved.
//

import UIKit

class RoomListVC: UIViewController {

    var roomList: UITableView!
    let roomCellID = "RoomListCell"
    var rooms = ["Atrium 1", "Atrium 2", "Atrium 3", "Atrium 4"]
    var emptySeats = [10, 20, 5, 15]

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white
        addTable()
    }
    
    func addTable() {
        roomList = UITableView()
        view.addSubview(roomList)
        roomList.translatesAutoresizingMaskIntoConstraints = false
        roomList.topAnchor.constraint(equalTo: view.topAnchor).isActive = true
        roomList.leftAnchor.constraint(equalTo: view.leftAnchor).isActive = true
        roomList.bottomAnchor.constraint(equalTo: view.bottomAnchor).isActive = true
        roomList.rightAnchor.constraint(equalTo: view.rightAnchor).isActive = true
        roomList.dataSource = self
        roomList.delegate = self
        roomList.register(UITableViewCell.self, forCellReuseIdentifier: roomCellID)
    }
}


extension RoomListVC: UITableViewDelegate {
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 80
    }
}

extension RoomListVC: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return rooms.count
    }
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: roomCellID, for: indexPath)
        let roomNameLbl = UILabel()
        roomNameLbl.text = rooms[indexPath.row]
        roomNameLbl.font = UIFont(name: "HelveticaNeue-Bold", size: 18)
        let emptySeatsLbl = UILabel()
        let emptySeatsCount = emptySeats[indexPath.row]
        emptySeatsLbl.text = "\(emptySeatsCount) Seats"
        emptySeatsLbl.font = UIFont(name: "HelveticaNeue-Light", size: 16)
        if (emptySeatsCount > 10) {
            emptySeatsLbl.textColor = confirmGreen
        } else {
            emptySeatsLbl.textColor = disabledRed
        }
        let contentStackView = UIStackView(arrangedSubviews: [roomNameLbl,emptySeatsLbl])
        cell.addSubview(contentStackView)
        contentStackView.translatesAutoresizingMaskIntoConstraints = false
        
        NSLayoutConstraint.activate([
            contentStackView.leadingAnchor.constraint(equalTo: cell.leadingAnchor, constant: 10),
            contentStackView.trailingAnchor.constraint(equalTo: cell.trailingAnchor, constant: -10),
            contentStackView.topAnchor.constraint(equalTo: cell.topAnchor, constant: 10),
            contentStackView.bottomAnchor.constraint(equalTo: cell.bottomAnchor, constant: 10)
        ])
        
//        cell.textLabel?.text = characters[indexPath.row]
        cell.selectionStyle = .blue
        return cell
    }
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        self.present(RoomSeatsVC(), animated: true)
    }
}



