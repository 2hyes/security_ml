//
//  ViewController.swift
//  FlaskApp
//
//  Created by Sue Cho on 2020/09/19.
//  Copyright © 2020 Sue Cho. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var resultLabel: UILabel!
    @IBOutlet weak var getButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }

    @IBAction func getButtonPressed(_ sender: Any) {
        // receive data from the server
        let numberOfFields: Int = 3
        let result: String = "Yes"
        
        NetworkHelper.shared.getData(numberOfFields: numberOfFields, result: result, completion: { obj in
            guard let receivedResult = obj.result else {
                return
            }
            DispatchQueue.main.async {
                self.resultLabel.text = receivedResult
            }
        })
    }
    
}

