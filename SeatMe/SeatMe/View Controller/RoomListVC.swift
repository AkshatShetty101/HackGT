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
    var characters = ["Atrium 1", "Atrium 2", "Atrium 3", "Atrium 4"]

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
    
}

extension RoomListVC: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return characters.count
    }
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
      let cell = tableView.dequeueReusableCell(withIdentifier: roomCellID, for: indexPath)
        cell.backgroundColor = .orange
      cell.textLabel?.text = characters[indexPath.row]
      return cell
    }
}
