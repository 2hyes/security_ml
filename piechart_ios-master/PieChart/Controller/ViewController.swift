//
//  ViewController.swift
//  FlaskApp
//
//  Created by Sue Cho on 2020/09/19.
//  Copyright © 2020 Sue Cho. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet var resultLabel: UILabel!
    @IBOutlet var getButton: UIButton!
    @IBOutlet var pieChartView: PieChartView!
    
    override func viewDidLoad() {
        super.viewDidLoad() 
    }

    
    private func receivePredResutFromServer(completion: @escaping ([Int]) -> Void){
        // receive data from the server
        let numberOfFields: Int = 0
        let results: [String] = [""]
        var resultCount = [Int]()
        var isComplete: Bool = false
        
        NetworkHelper.shared.getData(numberOfFields: numberOfFields, results: results, completion: { obj in
            guard let receivedResult = obj.results else {
                return
            }
            
            let normal = receivedResult.filter{ return $0 == "Normal"}
            let abnormal = receivedResult.filter { return $0 != "Normal"}
            resultCount.append(normal.count)
            resultCount.append(abnormal.count)
            DispatchQueue.main.async {
                self.resultLabel.text = "\(normal.count) \(abnormal.count)"
            }
            
            completion(resultCount) // type inference (maybe?)
        })
    }
    
    
    @IBAction func getButtonPressed(_ sender: Any) {
        receivePredResutFromServer { (data) in
            let sumOfData = Float(data.reduce(0, +))
            self.pieChartView.slices = [
                Slice(percent: CGFloat( Float(data[0]) / sumOfData ), color: UIColor.red),
                Slice(percent: CGFloat( Float(data[1]) / sumOfData ), color: UIColor.blue)
            ]
            DispatchQueue.main.async {
                self.pieChartView.animateChart()
            }
        }
    }
    
}

